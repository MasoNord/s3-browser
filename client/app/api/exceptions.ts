export const ERROR_MESSAGES = {
  APPLICATION_ERROR: "Ошибка приложения",
  INFRASTRUCTURE_ERROR: "Ошибка инфраструктуры",

  COMMIT_ERROR: "Ошибка сохранения данных",
  FLUSH_ERROR: "Ошибка синхронизации данных",
  ROLLBACK_ERROR: "Ошибка отката транзакции",

  S3_CONNECTION_ERROR: "Ошибка S3 соединения",

  S3_CLIENT_CREATION_ERROR:
    "Не удалось создать подключение к S3",

  S3_UNKNOWN_SERVICE_ERROR:
    "Неизвестный S3 сервис",

  S3_CONNECTION_NOT_FOUND:
    "S3 подключение не найдено",

  S3_CONNECTION_CLOSE_ERROR:
    "Не удалось закрыть S3 подключение",

  S3_CONNECTION_RESTORE_ERROR:
    "Не удалось восстановить S3 подключение",

  S3_IDLE_CONNECTION_CLEANUP_ERROR:
    "Ошибка очистки неактивных соединений",

  S3_BACKGROUND_TASK_ERROR:
    "Ошибка фоновой задачи",

  S3_PING_ERROR:
    "Ошибка проверки соединения",

  S3_INVALID_CONNECTION_CONFIG:
    "Некорректная конфигурация S3",

  AUTHENTICATION_ERROR:
    "Требуется авторизация",

  PERMISSION_DENIED:
    "Недостаточно прав",

  VALIDATION_ERROR:
    "Ошибка валидации данных",

  NETWORK_ERROR:
    "Ошибка сети",

  TIMEOUT_ERROR:
    "Превышено время ожидания",

  UNHANDLED_EXCEPTION:
    "Неизвестная ошибка"
} as const

export type ErrorCode = keyof typeof ERROR_MESSAGES