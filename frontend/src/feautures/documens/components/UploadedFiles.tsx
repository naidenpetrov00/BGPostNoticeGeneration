import { Button, Chip, Stack } from "@mui/material";

import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import type { SetStateAction } from "react";
import type { UploadStatus } from "../../../types/file";
import { useSendCSV } from "../api/sendCsvAndReceivePdf";

interface UploadFile {
  file: File | null;
  status: UploadStatus;
  setStatus: React.Dispatch<SetStateAction<UploadStatus>>;
  setErrors: React.Dispatch<SetStateAction<string[]>>;
  setFile: React.Dispatch<SetStateAction<File | null>>;
}

const UploadFiles = ({
  file,
  status,
  setStatus,
  setErrors,
  setFile,
}: UploadFile) => {
  const sendCsvMutation = useSendCSV({
    mutationConfig: {
      onSuccess(data) {
        const fileUrl = `${import.meta.env.VITE_APP_API_URL}${
          data.download_url
        }?t=${Date.now()}`;
        const link = document.createElement("a");
        link.href = fileUrl;
        link.download = "notices_and_envelopes.zip";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setStatus("success");
      },
      onError(error: Error) {
        setStatus("error");
        setErrors([error.message]);
      },
    },
  });

  const handleFileUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    sendCsvMutation.mutate({ data: { file } });
  };

  const clearFile = () => {
    setFile(null);
    setErrors([]);
  };
  return (
    <Stack
      direction="row"
      spacing={1}
      alignItems="center"
      justifyContent="space-between"
    >
      {file ? (
        <Chip
          color="primary"
          label={file.name}
          onDelete={clearFile}
          deleteIcon={<DeleteOutlineIcon />}
        />
      ) : (
        <Chip color="primary" label="No file selected" />
      )}
      <Button
        onClick={handleFileUpload}
        variant="contained"
        disabled={status == "uploading" || !file}
      >
        {status == "uploading" ? "Uploading..." : "Upload"}
      </Button>
    </Stack>
  );
};

export default UploadFiles;
