import { useCallback, useState, type SetStateAction } from "react";

import { Box, Button, Paper, Stack, Typography } from "@mui/material";
import { PairMode, type UploadStatus } from "../../../../types/file";
import { fileUploaderStyles } from "./FileUploader.styles";
import { useDropzone, type FileRejection } from "react-dropzone";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import {
  ACCEPTED,
  mapRejectionMessage,
  MAX_SIZE_BYTES,
} from "../../../../config/files";
import UploadedFiles from "../UploadedFiles";
import FileDropError from "../FileDropError";
import GenerateModePicker from "./GenerateModePicker";

const FileUploader = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<UploadStatus>("idle");
  const [errors, setErrors] = useState<string[]>([]);
  const [pairMode, setPairMode] = useState<PairMode>(PairMode.single);
  const onDrop = useCallback((acceptedFiles: SetStateAction<File | null>[]) => {
    setFile(acceptedFiles[0]);
    setErrors([]);
  }, []);
  const onDropRejected = useCallback((fileRejections: FileRejection[]) => {
    const msgs = fileRejections.flatMap(mapRejectionMessage);
    setErrors(msgs);
    setFile(null);
  }, []);

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
    open,
  } = useDropzone({
    onDrop,
    onDropRejected,
    accept: ACCEPTED,
    maxFiles: 1,
    multiple: false,
    maxSize: MAX_SIZE_BYTES,
    noClick: true,
  });

  return (
    <Box sx={fileUploaderStyles.container}>
      <Stack spacing={2}>
        <Paper
          variant="outlined"
          {...getRootProps()}
          sx={fileUploaderStyles.dropzone(
            isDragActive,
            isDragReject,
            isDragAccept
          )}
        >
          <input {...getInputProps()} />
          <CloudUploadIcon fontSize="large" />
          <Typography variant="h6" sx={fileUploaderStyles.caption}>
            {isDragActive
              ? "Drop the file here"
              : "Drag & drop a file here or click to browse"}
          </Typography>
          <Button
            onClick={open}
            sx={fileUploaderStyles.browseButton}
            variant="contained"
          >
            Browse files
          </Button>
          <Typography
            variant="caption"
            display="block"
            sx={fileUploaderStyles.caption}
          >
            Max size 25MB.
          </Typography>
          <GenerateModePicker pairMode={pairMode} setPairMode={setPairMode} />
        </Paper>

        <UploadedFiles
          file={file}
          pairMode={pairMode}
          setErrors={setErrors}
          setStatus={setStatus}
          setFile={setFile}
          status={status}
        />
        {errors.length > 0 && <FileDropError errors={errors} />}
      </Stack>
    </Box>
  );
};

export default FileUploader;
