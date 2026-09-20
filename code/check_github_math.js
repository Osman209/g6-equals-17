// Render every math span the way GitHub does, and inspect the output.
//
// COVERS the papers' rendering. Run it before any push that touches a math-bearing file.
//
// Three separate failure modes are checked, because a span can pass one and fail another:
//   (a) markdown strips a backslash before ASCII punctuation BEFORE KaTeX sees the span,
//       so \{ arrives as a bare { and the braces silently vanish with no error;
//   (b) GitHub's KaTeX deployment refuses macros a local KaTeX allows, \operatorname
//       being the one that has actually bitten;
//   (c) a span can render without raising and still say the wrong thing — a lost
//       subscript, a vanished brace.
//
// It also counts expressions per file. GitHub stops rendering math after roughly 1,800
// expressions in one file and prints "Unable to render expression" for everything after.
//
// Usage:  node code/check_github_math.js papers/*.md README.md
// It exits 2 when given no files, because a checker that silently passes by being
// invoked wrongly is worse than no checker.

const fs = require("fs");
const katex = require("katex");

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error("no files given; refusing to report a pass on zero files");
  process.exit(2);
}

// GitHub escapes a backslash before ANY ASCII punctuation. Use the full set, not a subset.
const ESCAPABLE = /\\([!-\/:-@\[-`{-~])/g;
const DENY = [
  "operatorname", "\\rm ", "\\bf ", "\\it ", "\\sf ", "\\tt ", "\\cal ",
  "mathchoice", "\\def", "\\newcommand", "\\href", "\\includegraphics",
];

let problems = 0;

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  const spans = [];
  const re = /\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    spans.push({ body: m[1] !== undefined ? m[1] : m[2], display: m[1] !== undefined });
  }

  let stripped = 0, failed = 0, silent = 0, denied = 0;

  for (const span of spans) {
    if (ESCAPABLE.test(span.body)) {
      ESCAPABLE.lastIndex = 0;
      stripped++;
      problems++;
      console.log(`${file}: escape stripped before KaTeX: ${span.body.slice(0, 70)}`);
      continue;
    }
    for (const token of DENY) {
      if (span.body.includes(token)) {
        denied++;
        problems++;
        console.log(`${file}: denied macro ${token.trim()}: ${span.body.slice(0, 70)}`);
      }
    }
    let html;
    try {
      html = katex.renderToString(span.body, { displayMode: span.display, throwOnError: true });
    } catch (err) {
      failed++;
      problems++;
      console.log(`${file}: render failure: ${span.body.slice(0, 70)} -- ${err.message}`);
      continue;
    }
    // (c) meaning checks: a lost subscript, or a brace group written where \lbrace was meant.
    // {,} and {:} are KaTeX spacing groups, not content; remove them before judging.
    const probe = span.body.replace(/\{[,:;]\}/g, "");
    if (/\}\d/.test(probe)) {
      silent++;
      problems++;
      console.log(`${file}: possible lost subscript: ${span.body.slice(0, 70)}`);
    }
    // a brace group is legitimate after _, ^, or a macro name; only a standalone one is a risk
    if (/(^|[^\\a-zA-Z_^])\{[^{}]*,[^{}]*\}/.test(probe) && !probe.includes("\\lbrace")) {
      silent++;
      problems++;
      console.log(`${file}: bare brace group, braces will vanish: ${span.body.slice(0, 70)}`);
    }
    // a variable macro followed straight by a brace group is a subscript that lost its _
    if (/\\(alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|phi|chi|psi|omega|Gamma|Delta|Lambda|Sigma|Phi|Psi|Omega)\{/.test(probe)) {
      silent++;
      problems++;
      console.log(`${file}: variable macro followed by a brace group, lost subscript: ${span.body.slice(0, 70)}`);
    }
  }

  console.log(
    `${file}: ${spans.length} expressions, ${stripped} escape-stripped, ` +
    `${failed} render failures, ${denied} denied macros, ${silent} silent-risk`
  );
  if (spans.length > 1500) {
    console.log(`${file}: WARNING ${spans.length} expressions; GitHub stops rendering near 1,800`);
  }
}

console.log("TOTAL problems:", problems);
process.exit(problems === 0 ? 0 : 1);
