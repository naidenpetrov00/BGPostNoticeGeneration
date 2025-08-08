import { PDFDocument } from "pdf-lib";
import { checkIfBarcode } from "./utils.js";
import fontkit from "@pdf-lib/fontkit";
import fs from "fs";

const inputPath = process.argv[2];
const outputPath = process.argv[3];
const openSansFontPath = "./fonts/OpenSans-Regular.ttf";
const libreBarcode38TextFontPath = "./fonts/ttf/libre-barcode-39-text-latin-400-normal.ttf";

const run = async () => {
  const pdfBytes = fs.readFileSync(inputPath);
  const openSansFontBytes = fs.readFileSync(openSansFontPath);
  const libreBarcode38TextBytes = fs.readFileSync(libreBarcode38TextFontPath);
  const pdfDoc = await PDFDocument.load(pdfBytes);

  pdfDoc.registerFontkit(fontkit);

  const form = pdfDoc.getForm();
  const openSans = await pdfDoc.embedFont(openSansFontBytes, { subset: false });
  const libreBarcode38Text = await pdfDoc.embedFont(libreBarcode38TextBytes, {
    subset: false,
  });

  const fields = form.getFields();

  for (const field of fields) {
    const name = field.getName();

    const type = field.constructor.name;

    try {
      if (type === "PDFTextField") {
        const value = field.getText();
        ``;
        const fontToEmbed = checkIfBarcode(value) ? libreBarcode38Text : openSans;
        field.setText(value);
        field.updateAppearances(fontToEmbed);
      }

      if (type === "PDFCheckBox") {
        if (field.isChecked()) field.check();
        else field.uncheck();
      }

      if (type === "PDFRadioGroup") {
        const val = field.getSelected();
        if (val) field.select(val);
      }
    } catch (err) {
      console.warn(`⚠️ Failed to update field ${name}:`, err.message);
    }
  }

  const fixedPdfBytes = await pdfDoc.save();
  fs.writeFileSync(outputPath, fixedPdfBytes);
  console.log("✅ Appearance regeneration complete.");
};

run().catch(console.error);
