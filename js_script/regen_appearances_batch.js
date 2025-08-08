import { PDFDocument } from "pdf-lib";
import fontkit from "@pdf-lib/fontkit";
import fs from "fs";

// usage: node regen-appearances-batch.js file1.pdf file2.pdf ...
const files = process.argv.slice(2);
if (!files.length) {
  console.error("Usage: node regen-appearances-batch.js <pdf...>");
  process.exit(1);
}

const openSansPath = "./fonts/OpenSans-Regular.ttf";
const libreBarcode38TextFontPath =
  "./fonts/ttf/libre-barcode-39-text-latin-400-normal.ttf";

const isBarcode = (v) =>
  typeof v === "string" && v.startsWith("*") && v.endsWith("*");

const main = async () => {
  // read fonts ONCE
  const openSansBytes = fs.readFileSync(openSansPath);
  const libreBarcode38TextBytes = fs.readFileSync(libreBarcode38TextFontPath);

  for (const pdfPath of files) {
    try {
      const pdfBytes = fs.readFileSync(pdfPath);
      const pdfDoc = await PDFDocument.load(pdfBytes);
      pdfDoc.registerFontkit(fontkit);

      const openSans = await pdfDoc.embedFont(openSansBytes); // let it subset (faster, smaller)
      let libreBarcode38Text = await pdfDoc.embedFont(libreBarcode38TextBytes);

      const form = pdfDoc.getForm();
      for (const field of form.getFields()) {
        if (field.constructor.name === "PDFTextField") {
          const raw = field.getText();
          const value = typeof raw === "string" ? raw : "";
          const fontToUse = isBarcode(value) ? libreBarcode38Text : openSans;
          field.setText(value); // re-assign to trigger appearance
          field.updateAppearances(fontToUse); // regenerate /AP
        } else if (field.constructor.name === "PDFCheckBox") {
          field.isChecked() ? field.check() : field.uncheck();
        } else if (field.constructor.name === "PDFRadioGroup") {
          const sel = field.getSelected();
          if (sel) field.select(sel);
        }
      }

      fs.writeFileSync(pdfPath, await pdfDoc.save()); // overwrite in place
      console.log(`✅ Regenerated: ${pdfPath}`);
    } catch (err) {
      console.error(`❌ Failed: ${pdfPath} — ${err.message}`);
    }
  }
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
