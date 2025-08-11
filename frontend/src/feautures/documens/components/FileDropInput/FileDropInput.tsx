// import {
//   Box,
//   Button,
//   Chip,
//   LinearProgress,
//   Paper,
//   Stack,
//   Typography,
// } from "@mui/material";
// import Dropzone, { type FileRejection } from "react-dropzone";
// import { useState } from "react";

// import CloudUploadIcon from "@mui/icons-material/CloudUpload";
// import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";

// export default function FileDropInput() {
//   return (
//     <Box sx={{ maxWidth: 560, mx: "auto", mt: 4 }}>
//       <Stack spacing={2}>
//         <Dropzone
//           multiple={false}
//           maxFiles={1}
//           // accept={{ "application/pdf": [".pdf"], "image/*": [] }}
//         >
//           {({
//             getRootProps,
//             getInputProps,
//             isDragActive,
//             isDragAccept,
//             isDragReject,
//             open,
//           }) => (
//             <Paper
//               variant="outlined"
//               {...getRootProps()}
//               sx={{
//                 p: 4,
//                 textAlign: "center",
//                 borderStyle: "dashed",
//                 bgcolor: isDragActive ? "action.hover" : "background.paper",
//                 borderColor: isDragReject
//                   ? "error.main"
//                   : isDragAccept
//                   ? "success.main"
//                   : "divider",
//                 cursor: "pointer",
//               }}
//             >
//               <input {...getInputProps()} />
//               <CloudUploadIcon fontSize="large" />
//               <Typography variant="h6" sx={{ mt: 1 }}>
//                 {isDragActive
//                   ? "Drop the file here"
//                   : "Drag & drop a file here or click to browse"}
//               </Typography>
//               <Button onClick={open} sx={{ mt: 2 }} variant="contained">
//                 Browse files
//               </Button>
//               <Typography
//                 variant="caption"
//                 color="text.secondary"
//                 display="block"
//                 sx={{ mt: 1 }}
//               >
//                 Max size 25MB. Change accepted types/limits in code.
//               </Typography>
//             </Paper>
//           )}
//         </Dropzone>

//         <Stack
//           direction="row"
//           spacing={1}
//           alignItems="center"
//           justifyContent="space-between"
//         >
//           {file ? (
//             <Chip
//               label={file.name}
//               onDelete={clearFile}
//               deleteIcon={<DeleteOutlineIcon />}
//             />
//           ) : (
//             <Chip label="No file selected" />
//           )}
//           <Button
//             onClick={handleUpload}
//             variant="contained"
//             disabled={uploading || !file}
//           >
//             {uploading ? "Uploading..." : "Upload"}
//           </Button>
//         </Stack>

//         {uploading && <LinearProgress />}

//         {error && (
//           <Typography variant="body2" color="error">
//             {error}
//           </Typography>
//         )}

//         {message && (
//           <Typography
//             variant="body2"
//             color={message.includes("failed") ? "error" : "success.main"}
//           >
//             {message}
//           </Typography>
//         )}
//       </Stack>
//     </Box>
//   );
// }
