import type { FileRejection } from "react-dropzone";

export const MAX_SIZE_BYTES = 25 * 1024 * 1024;

export const ACCEPTED = {
  "text/csv": [".csv"],
  "application/vnd.ms-excel": [".xls"],
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
    ".xlsx",
  ],
  "application/vnd.oasis.opendocument.spreadsheet": [".ods"],
};

export const mapRejectionMessage = (rej: FileRejection) => {
  const { file, errors } = rej;
  return errors.map((e) => {
    switch (e.code) {
      case "file-invalid-type":
        return `Неподдържан тип: "${file.name}". Разрешени са: CSV, XLS, XLSX, ODS.`;
      case "file-too-large":
        return `Файлът "${file.name}" е твърде голям (${humanFileSize(
          file.size
        )}). Максимумът е ${humanFileSize(MAX_SIZE_BYTES)}.`;
      case "file-too-small":
        return `Файлът "${file.name}" е твърде малък.`;
      case "too-many-files":
        return `Може да качите само един файл.`;
      default:
        return `Грешка при "${file.name}": ${e.message}`;
    }
  });
};

const humanFileSize = (bytes: number) => {
  if (bytes < 1024) return `${bytes} B`;
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  const sizes = ["B", "KB", "MB", "GB", "TB"];
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
};
