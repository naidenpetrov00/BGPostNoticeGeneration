import { Alert, AlertTitle } from "@mui/material";

import { fileUploaderStyles } from "./FileDrop/FileUploader.styles";

interface FileDropErrorProps {
  errors: string[];
}

const FileDropError = ({ errors }: FileDropErrorProps) => {
  return (
   
    <Alert severity="error">
      <AlertTitle>Грешка при качване</AlertTitle>
      <ul style={fileUploaderStyles.errorList}>
        {errors.map((msg, idx) => (
          <li key={idx}>{msg}</li>
        ))}
      </ul>
    </Alert>
  );
};

export default FileDropError;
