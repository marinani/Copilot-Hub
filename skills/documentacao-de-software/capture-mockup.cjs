/**
 * Generic script to capture mockups from HTML using Playwright
 * Usage: node capture-mockup.cjs <input-html-path> <output-png-path>
 *
 * Exit codes:
 *   0 — success
 *   1 — parameter/argument error
 *   2 — dependency error (Playwright not installed)
 *   3 — generation error
 */

function checkDependencies() {
    try {
        require('playwright');
    } catch {
        console.error('DEPENDENCY ERROR: Playwright is not installed.');
        console.error('Install it with: npm install playwright');
        console.error('Then install browsers: npx playwright install chromium');
        process.exit(2);
    }
}

async function capture() {
    checkDependencies();

    const { chromium } = require('playwright');
    const path = require('path');
    const fs = require('fs');

    const args = process.argv.slice(2);
    if (args.length !== 2) {
        console.error('ERROR: Invalid parameters.');
        console.error('Usage: node capture-mockup.cjs <input-html-path> <output-png-path>');
        console.error('Example: node capture-mockup.cjs ./mockup.html ./output.png');
        process.exit(1);
    }

    const inputHtml = path.resolve(args[0]);
    const outputPng = path.resolve(args[1]);

    if (!fs.existsSync(inputHtml)) {
        console.error(`ERROR: Input HTML file not found: ${inputHtml}`);
        process.exit(1);
    }

    // Ensure output directory exists
    const outputDir = path.dirname(outputPng);
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
        console.log(`Created output directory: ${outputDir}`);
    }

    console.log(`Loading: file://${inputHtml}`);
    let browser;
    try {
        browser = await chromium.launch({ headless: true });
        const page = await browser.newPage();

        // HD resolution for good visibility
        await page.setViewportSize({ width: 1280, height: 720 });
        await page.goto(`file://${inputHtml}`, { waitUntil: 'networkidle' });

        // Take screenshot
        await page.screenshot({ path: outputPng, fullPage: false });
        await browser.close();

        // Validate output file
        if (!fs.existsSync(outputPng)) {
            console.error(`ERROR: Output file was not created: ${outputPng}`);
            process.exit(3);
        }

        const stats = fs.statSync(outputPng);
        console.log(`Visual mockup generated successfully at: ${outputPng}`);
        console.log(`File size: ${(stats.size / 1024).toFixed(1)} KB`);
    } catch (err) {
        if (browser) await browser.close().catch(() => {});
        console.error('ERROR: Failed to generate wireframe:', err.message);
        process.exit(3);
    }
}

capture();
