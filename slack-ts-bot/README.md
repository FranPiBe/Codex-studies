# Bot de Slack en TypeScript

Este directorio contiene un ejemplo minimalista de una aplicación de Slack escrita en TypeScript. La app expone un comando `/runmodel` que:

1. Invoca una función de AWS Lambda (que podría contener un modelo de ML).
2. Registra el resultado en una hoja de cálculo de Google Sheets.
3. Devuelve el payload a la persona que ejecutó el comando en Slack.

## Estructura del proyecto

- `src/index.ts`: código de la aplicación.
- `package.json`: dependencias y scripts de npm.
- `tsconfig.json`: configuración de TypeScript.
- `.gitignore`: exclusión de `node_modules` y variables de entorno.

## Configuración

1. **Variables de entorno**: crea un archivo `.env` con los siguientes valores:

```
SLACK_BOT_TOKEN=xxx
SLACK_SIGNING_SECRET=xxx
AWS_REGION=us-east-1
AWS_LAMBDA_FUNCTION=nombre-de-tu-funcion
GOOGLE_CLIENT_EMAIL=bot@project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
GOOGLE_SHEET_ID=tu_sheet_id
PORT=3000
```

2. **Instalación de dependencias**:

```
npm install
```

3. **Ejecución**:

```
npx ts-node src/index.ts
```

## Uso en proyectos más grandes

Este ejemplo puede integrarse como un microservicio dentro de una arquitectura mayor. El patrón de interacción es:

- Slack actúa como capa de interfaz para desencadenar la lógica.
- AWS procesa la solicitud o ejecuta un modelo.
- Google Sheets se usa como almacenamiento ligero o logging.

La misma estructura puede ampliarse para incluir bases de datos, colas de mensajes u otros servicios.
