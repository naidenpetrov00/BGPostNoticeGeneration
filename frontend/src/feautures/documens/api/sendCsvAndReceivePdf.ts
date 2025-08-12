import type { MutationConfig } from "../../../lib/reactQuery";
import type { ResultPdf } from "../../../types/api";
import { api } from "../../../lib/api-client";
import { useMutation } from "@tanstack/react-query";
import z from "zod";

export const sendCsvInputSchema = z.object({
  file: z.instanceof(File),
});

export type SendCsvInput = z.infer<typeof sendCsvInputSchema>;

export const sendCsvAndReceivePdf = async ({
  data,
}: {
  data: SendCsvInput;
}): Promise<ResultPdf> => {
  const formData = new FormData();
  formData.append("file", data.file);

  const response = await api.post("/process-csv", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    responseType: "blob",
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
