import { PDFDocument } from "pdf-lib";
import fontkit from "@pdf-lib/fontkit";
import fs from "fs";

const inputPath = process.argv[2];
const outputPath = process.argv[3];
const fontPath = "/home/naidenpetrov00/Fonts/OpenSans-Regular.ttf";

const run = async () => {
  const pdfBytes = fs.readFileSync(inputPath);
  const fontBytes = fs.readFileSync(fontPath);
  const pdfDoc = await PDFDocument.load(pdfBytes);

  // ✅ Register fontkit here
  pdfDoc.registerFontkit(fontkit);

  const form = pdfDoc.getForm();
  const embeddedFont = await pdfDoc.embedFont(fontBytes, { subset: false });

  const fields = form.getFields();

  for (const field of fields) {
    const name = field.getName();
    const type = field.constructor.name;

    try {
      if (type === "PDFTextField") {
        const value = field.getText();
        field.setText(value);
        field.updateAppearances(embeddedFont);
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
