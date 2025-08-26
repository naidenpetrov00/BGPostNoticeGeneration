import type { MutationConfig } from "../../../lib/reactQuery";
import  { PairMode } from "../../../types/file";
// import type { ResultPdf } from "../../../types/api";
import { api } from "../../../lib/api-client";
import { useMutation } from "@tanstack/react-query";
import z from "zod";

export const sendCsvInputSchema = z.object({
  file: z.instanceof(File),
  pairMode: z.enum(PairMode),
});

export type SendCsvInput = z.infer<typeof sendCsvInputSchema>;

export const sendCsvAndReceivePdf = async ({
  data,
}: {
  data: SendCsvInput;
}): Promise<{ download_url: string }> => {
  const formData = new FormData();
  formData.append("file", data.file);
  formData.append("mode", data.pairMode);

  const response = await api.post("/api/process-csv", formData, {
    headers: { "Content-Type": "multipart/form-data"},
    // responseType: "blob",
  });

  return response.data;
};

type UseSendCsvOptions = {
  mutationConfig?: MutationConfig<typeof sendCsvAndReceivePdf>;
};

export const useSendCSV = ({ mutationConfig }: UseSendCsvOptions) => {
  return useMutation({
    mutationFn: sendCsvAndReceivePdf,
    ...mutationConfig,
  });
};
