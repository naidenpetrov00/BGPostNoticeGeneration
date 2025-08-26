import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  Typography,
} from "@mui/material";

import type { PairMode } from "../../../../types/file";
import type { SetStateAction } from "react";

interface GenerateModePickerProps {
  pairMode: PairMode;
  setPairMode: React.Dispatch<SetStateAction<PairMode>>;
}

const GenerateModePicker = ({
  pairMode,
  setPairMode,
}: GenerateModePickerProps) => {
  return (
    <FormControl>
      <FormLabel id="demo-row-radio-buttons-group-label">
        <Typography color="textPrimary">Метод на комплектоване</Typography>
      </FormLabel>
      <RadioGroup
        value={pairMode}
        row
        aria-labelledby="demo-row-radio-buttons-group-label"
        name="row-radio-buttons-group"
        onChange={(_, val) => setPairMode(val as PairMode)}
      >
        <FormControlLabel value="single" control={<Radio />} label="Единични" />
        <FormControlLabel
          value="pair"
          control={<Radio />}
          label="Последователни"
        />
        <FormControlLabel
          value="compact"
          control={<Radio />}
          label="Комплектовани"
        />
      </RadioGroup>
    </FormControl>
  );
};

export default GenerateModePicker;
