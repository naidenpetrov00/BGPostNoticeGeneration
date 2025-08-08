export const checkIfBarcode = (value) =>
  typeof value === "string" && value.startsWith("*") && value.endsWith("*");
