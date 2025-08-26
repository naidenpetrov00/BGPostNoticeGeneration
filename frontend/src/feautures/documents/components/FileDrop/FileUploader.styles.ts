export const fileUploaderStyles = {
  container: { maxWidth: 560, mx: "auto", mt: 4 },
  dropzone: (isDragActive: boolean, isDragReject: boolean, isDragAccept: boolean) => ({
    p: 4,
    textAlign: "center",
    borderStyle: "dashed",
    bgcolor: isDragActive ? "action.hover" : "background.paper",
    borderColor: isDragReject
      ? "error.main"
      : isDragAccept
      ? "success.main"
      : "divider",
    cursor: "pointer",
  }),
  browseButton: { mt: 2 },
  caption: { mt: 1 },
  fileRow: {
    direction: "row",
    spacing: 1,
    alignItems: "center",
    justifyContent: "space-between",
  },
  errorList: {
    margin: 0,
    paddingLeft: 18,
  },
};
