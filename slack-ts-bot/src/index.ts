import { App } from "@slack/bolt";
import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";
import { google } from "googleapis";

// Initialize Slack Bolt app
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
});

// Slash command handler
app.command("/runmodel", async ({ command, ack, respond }) => {
  await ack();

  try {
    const payload = await invokeModel(command.text || "");
    await logToSheet(payload);
    await respond(`Modelo ejecutado. Payload: ${payload}`);
  } catch (err: any) {
    await respond(`Error al ejecutar el modelo: ${err.message}`);
  }
});

async function invokeModel(input: string): Promise<string> {
  const client = new LambdaClient({ region: process.env.AWS_REGION });
  const command = new InvokeCommand({
    FunctionName: process.env.AWS_LAMBDA_FUNCTION,
    Payload: Buffer.from(JSON.stringify({ input })),
  });
  const response = await client.send(command);
  const payload = response.Payload ? Buffer.from(response.Payload).toString() : "";
  return payload;
}

async function logToSheet(payload: string) {
  const auth = new google.auth.GoogleAuth({
    credentials: {
      client_email: process.env.GOOGLE_CLIENT_EMAIL,
      private_key: process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, "\n"),
    },
    scopes: ["https://www.googleapis.com/auth/spreadsheets"],
  });

  const sheets = google.sheets({ version: "v4", auth });
  await sheets.spreadsheets.values.append({
    spreadsheetId: process.env.GOOGLE_SHEET_ID,
    range: "Sheet1!A:B",
    valueInputOption: "RAW",
    requestBody: { values: [[new Date().toISOString(), payload]] },
  });
}

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log("⚡️ Slack Bolt app is running!");
})();
