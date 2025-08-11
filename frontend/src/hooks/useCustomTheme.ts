import { type Theme, createTheme } from "@mui/material";

import { useMemo } from "react";

// const minCharcoal = '#73787C';
// const minGray = '#C5C6C7';
// const minPaleBlue = '#D7E5F0';
// const minBeige = '#C9AD93';
const colorPallete = {
  black: "#181C14",
  grey: "#3C3D37",
  green: "#697565",
  white: "#ECDFCC",
};

export const useCustomTheme = (): Theme => {
  return useMemo(() => {
    return createTheme({
      palette: {
        primary: { main: colorPallete.black },
        secondary: { main: colorPallete.green },
        background: { paper: colorPallete.grey },
        text: { primary: colorPallete.white, secondary: colorPallete.black },
      },
    });
  }, []);
};

// declare module '@mui/material/styles' {
//   interface Theme {
//     status: {
//       danger: string;
//     };
//   }
//   // allow configuration using `createTheme()`
//   interface ThemeOptions {
//     status?: {
//       danger?: string;
//     };
//   }
// }
