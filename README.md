# 🚀 DeploySlim: Supercharge Website Speed & SEO with Brotli & Gzip Compression (Free!)

### Optimized for All Websites & Runs Seamlessly on Linux & Windows Build Servers

**Dramatically improve your website's performance and search engine rankings by automatically compressing your web assets (HTML, CSS, JavaScript, SVG, JSON, XML, WASM, and more) within your GitHub Actions workflow!** DeploySlim utilizes cutting-edge Brotli and widely compatible Gzip compression to significantly reduce file sizes. This results in lightning-fast load times, enhanced user experience, and a boost in SEO, regardless of your website's technology or your chosen build server environment on GitHub Actions.

_Seamlessly integrates with **any** website – static, dynamic, or built with any framework or generator. Runs flawlessly on **both Linux (`ubuntu-latest`) and Windows (`windows-latest`) build agents** provided by GitHub Actions._

## ✨ Key Benefits

- **⚡️ Universal Website Optimization:** Accelerate the loading speed of **any** website by reducing the size of compressible text-based assets.
- **📈 Maximize SEO Performance:** Achieve better search engine visibility. Faster loading times are a critical ranking factor for Google and other search engines.
- **💾 Reduce Bandwidth Costs:** Lower file sizes translate to less data transfer during deployment and for your website visitors, saving valuable bandwidth.
- **✅ Industry-Leading Compression:** Leverages both Brotli (`br`) for the highest compression ratios and Gzip (`gz`) for excellent browser compatibility.
- **🧠 Intelligent Asset Handling:** Automatically detects and compresses relevant text-based web files based on their MIME types.
- **⚙️ Granular Control:** Easily configure compression levels for both Brotli (0-11) and Gzip (0-9) to fine-tune the balance between file size and compression speed.
- **🛠️ Effortless Integration:** Add to your existing GitHub Actions workflow in minutes with minimal configuration.
- ****💻 Cross-Platform Compatibility:** Designed to run smoothly on both **Linux (`ubuntu-latest`)** and **Windows (`windows-latest`)** virtual environments provided by GitHub Actions.**
- **🆓 Completely Free:** DeploySlim is a free and open-source GitHub Action.

## ⚙️ Simple Usage in Your Workflow

Integrate DeploySlim into your deployment workflow file (e.g., `deploy.yml`) with these straightforward steps:

```yaml
name: Deploy with Compression

on: [push] # Or your preferred workflow trigger (e.g., pull_request, release)

jobs:
  deploy:
    runs-on: ubuntu-latest # Or use `windows-latest` for Windows builds

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # ... Your website build process (e.g., npm build, Hugo, Jekyll) ...

      - name: Compress Assets with DeploySlim
        uses: CornerstoneCode/DeploySlim@v1
        with:
          directory: './public' # ⚠️ Replace with the path to your website's build output directory (e.g., public, dist, _site)
          algorithms: 'br,gz' # Optional: Specify compression algorithms (default: br,gz)
          brotli-level: 9      # Optional: Set Brotli compression level (0-11, default: 6) - Higher level = smaller files, longer processing
          gzip-level: 7        # Optional: Set Gzip compression level (0-9, default: 6) - Higher level = smaller files, longer processing

      # ... Your website deployment steps (e.g., deploying to Netlify, Vercel, AWS S3) ...
