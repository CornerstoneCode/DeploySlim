# DeploySlim

**Web asset compression for lightning-fast deployments**

This GitHub Action automatically compresses web assets in your repository using Brotli and Gzip to minimize file sizes and maximize loading speed. Compatible with any web framework or static site.

## Features

- Multi-algorithm compression (Brotli, Gzip)
- Smart content-type detection (compresses text-based web assets)
- Configurable compression levels for both Brotli and Gzip
- Designed for use in GitHub Actions on Linux and Windows runners

## Usage

To use DeploySlim in your GitHub Actions workflow, add the following step to your `deploy.yml` file (or any other workflow file):

```yaml
name: Deploy with Compression

on: [push] # Or your preferred trigger

jobs:
  deploy:
    runs-on: ubuntu-latest # Or windows-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Compress Assets with DeploySlim
        uses: CornerstoneCode/deploy-slim@v1  
        with:
          directory: 'public' # Replace 'public' with the path to your web assets directory
          algorithms: 'br,gz' # Optional: Specify compression algorithms (default: br,gz)
          brotli-level: 9     # Optional: Set Brotli compression level (0-11, default: 6)
          gzip-level: 7       # Optional: Set Gzip compression level (0-9, default: 6)

      # Add your deployment steps below this, for example:
      # - name: Deploy to hosting
      #   run: echo "Deploying compressed assets..."

**Note:** Replace `your-github-username/deploy-slim@v1` with the actual path to your action in the GitHub Marketplace once you publish it. Also, adjust the version tag (`@v1`) to the specific version you are using.

## Inputs

The DeploySlim action accepts the following inputs:

| Name           | Description                                                                 | Required | Default   |
|----------------|-----------------------------------------------------------------------------|----------|-----------|
| `directory`    | The directory containing the web assets to compress.                        | Yes      |           |
| `algorithms`   | Comma-separated list of compression algorithms to use (`br`, `gz`).         | No       | `br,gz`   |
| `brotli-level` | Brotli compression level (an integer between 0 and 11, where 11 is best).   | No       | `6`       |
| `gzip-level`   | Gzip compression level (an integer between 0 and 9, where 9 is best).       | No       | `6`       |

## Example Workflow

This example workflow demonstrates how to use DeploySlim to compress assets in a `public` directory when code is pushed to the repository:

```yaml
name: Deploy with Compression

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Compress Assets
        uses: CornerstoneCode/deploy-slim@v1
        with: 
          algorithms: 'br' # Only use Brotli compression
          brotli-level: 11
 
```

In this example, only Brotli compression is used at the highest level (11) for the assets in the `public` directory before deploying to GitHub Pages.