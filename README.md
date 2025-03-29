# DeploySlim

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/release/YourUsername/deployslim.svg)](https://GitHub.com/YourUsername/deployslim/releases/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/YourUsername/deployslim/CI)](https://github.com/YourUsername/deployslim/actions)

**Web asset compression for lightning-fast deployments**

Automatically compress web assets using Brotli and Gzip to minimize file sizes and maximize loading speed. Compatible with any web framework or static site.

## 🚀 Getting Started

Add this to your GitHub workflow:

```yaml
- name: Compress web assets
  uses: YourUsername/deployslim@v1
  with:
    directory: 'dist'           # Directory containing your build assets
    compression-level: 'high'   # Options: low, medium, high, extreme
    generate-report: true       # Generates compression statistics
```

## ⚙️ Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `directory` | Path to your build output directory | `dist` |
| `compression-level` | Compression intensity | `medium` |
| `algorithms` | Comma-separated list of algorithms to use | `brotli,gzip` |
| `extensions` | File extensions to compress | `js,css,html,svg,json` |
| `exclude` | Files/patterns to exclude from compression | `*.min.js,*.min.css` |
| `generate-report` | Create a compression report | `false` |

## 📊 Example Report

```
DeploySlim Compression Report
-----------------------------
Original size: 2,456 KB
Compressed size: 876 KB
Reduction: 64.3%

File breakdown:
main.js: 1,240 KB → 389 KB (68.6%)
styles.css: 560 KB → 187 KB (66.6%)
vendor.js: 656 KB → 300 KB (54.3%)
```

## 🔍 How It Works

DeploySlim analyzes your web assets and applies optimal compression algorithms:

1. Detects file types and selects appropriate compression strategy
2. Applies Brotli compression at configurable levels
3. Creates Gzip fallbacks for older browsers
4. Preserves original files and adds compressed versions
5. Generates detailed compression statistics

## 🛠️ Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
