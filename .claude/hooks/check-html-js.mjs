#!/usr/bin/env node
// HTML 파일을 수정할 때마다 그 안의 인라인 JavaScript 문법을 검사하는 훅.
// 문법 오류가 있으면 stderr로 알리고 exit 2 → Claude가 즉시 인지하고 고칠 수 있다.
// (문법만 검사한다. document/window 같은 브라우저 전역은 검사 대상이 아니므로 안전하다.)

import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

function readStdin() {
  try {
    return readFileSync(0, 'utf8');
  } catch {
    return '';
  }
}

let filePath = '';
try {
  const input = JSON.parse(readStdin() || '{}');
  filePath = input?.tool_input?.file_path || '';
} catch {
  process.exit(0); // 입력을 못 읽으면 조용히 통과 (작업을 막지 않는다)
}

// HTML 파일이 아니면 아무것도 하지 않는다.
if (!filePath || !filePath.toLowerCase().endsWith('.html')) process.exit(0);

let html = '';
try {
  html = readFileSync(filePath, 'utf8');
} catch {
  process.exit(0);
}

// src= 없는 인라인 <script> 블록만 추출 (CDN 스크립트는 제외).
const blocks = [];
const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m;
while ((m = re.exec(html)) !== null) {
  if (/\bsrc\s*=/i.test(m[1])) continue; // 외부 스크립트는 건너뜀
  blocks.push(m[2]);
}

if (blocks.length === 0) process.exit(0);

const tmp = join(tmpdir(), `htmljs-${process.pid}.js`);
try {
  writeFileSync(tmp, blocks.join('\n;\n'), 'utf8');
  execFileSync(process.execPath, ['--check', tmp], { stdio: 'pipe' });
} catch (err) {
  const msg = (err.stderr ? err.stderr.toString() : err.message || '').trim();
  console.error(`⚠️  ${filePath} 의 JavaScript 문법 오류로 보입니다. 배포 전에 고쳐야 화면이 하얗게 죽지 않습니다:\n${msg}`);
  try { unlinkSync(tmp); } catch {}
  process.exit(2); // Claude에게 오류를 전달
} finally {
  try { unlinkSync(tmp); } catch {}
}

process.exit(0);
