# DeploySlim

### Works seamlessly on Linux and Windows

**This GitHub Action automatically optimize your website by compressing HTML, CSS, JavaScript, and more within your GitHub Actions.**
_Compatible with any web framework or static site_
 

## Features
- Multi-algorithm compression (Brotli, Gzip)
- Smart content-type detection (compresses text-based web assets)
- Configurable compression levels for both Brotli and Gzip


## Example Workflow

To use DeploySlim in your GitHub Actions workflow, add the following step to your `deploy.yml` file (or any other workflow file):

```yaml
name: Deploy with Compression

on: [push] # Or your preferred trigger

jobs:
  deploy:
    runs-on: ubuntu-latest # Or `windows-latest` for Windows server
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Compress Assets with DeploySlim
        uses: CornerstoneCode/DeploySlim@v1 
        with: 
          algorithms: 'br,gz' # Optional: Specify compression algorithms (default: br,gz)
          brotli-level: 9     # Optional: Set Brotli compression level (0-11, default: 6)
          gzip-level: 7       # Optional: Set Gzip compression level (0-9, default: 6) 

## Inputs

The DeploySlim action accepts the following inputs:

| Name           | Description                                                                 | Required | Default   |
|----------------|-----------------------------------------------------------------------------|----------|-----------|
| `directory`    | Restricts compression to a single directory                                 | No      |           |
| `algorithms`   | Comma-separated list of compression algorithms to use (`br`, `gz`).         | No       | `br,gz`   |
| `brotli-level` | Brotli compression level (an integer between 0 and 11, where 11 is best).   | No       | `6`       |
| `gzip-level`   | Gzip compression level (an integer between 0 and 9, where 9 is best).       | No       | `6`       |
```
