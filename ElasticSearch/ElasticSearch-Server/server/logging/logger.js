/*
* @description
* This script initializes a logger using the Winston library.
* It creates a logger with a rotating file transport for log storage and a console transport for log output.
* Logs will be stored in the folder specified in the LOG_FILE_FOLDER environment variable.
* It is initialized with a log level based on the LOG_LEVEL environment variable.
* 
*/


import winston from 'winston';
import 'winston-daily-rotate-file';
import path from 'path';
import { dirname } from 'node:path';
// import { fileURLToPath } from 'node:url';
    
// const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * @class WinstonLogger
 * @description A Custom logging class for logging messages using the Winston library.
 * Initializes the logger with a rotating file transport for log storage and a console transport for log output.
 * The logger is configured to log messages with a timestamp and a JSON format.
 * The logger is initialized with a log level based on the LOG_LEVEL environment variable.
 */
class WinstonLogger {
    /**
     * @constructor
     * @description Create an instance of a WinstonLogger.
     * Initializes the logger with a rotating file transport for log storage and a console transport for log output.
     * The logger is configured to log messages with a timestamp and a JSON format.
     * The logger is initialized with a log level based on the LOG_LEVEL environment variable.
     * @param {string} filename - The name of the file to log to. Log file will be stored in the folder specified in the LOG_FILE_FOLDER environment variable.
     */
    constructor(filename) {
        // Create a logger that outputs log messages 
        // - in a JSON format.
        // - with a timestamp.
        // - only above a log level based on the LOG_LEVEL environment variable.
        // - with a rotating file transport for log storage and a console transport for log output.

        this._logger = winston.createLogger({
            level: process.env.LOG_LEVEL,
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            ),
            transports: [
                new winston.transports.Console(),
                // Log all logs to a file that rotates daily.
                new winston.transports.DailyRotateFile({ 
                    filename: path.join(process.env.LOG_FILE_FOLDER, `${filename}.log`),
                    datePattern: 'YYYY-MM-DD', 
                    zippedArchive: true,
                    maxSize: '10m', 
                    maxFiles: '3d' 
                }),
                // Log all error logs to a separate file that rotates daily.
                new winston.transports.DailyRotateFile({ 
                    filename: path.join(process.env.LOG_FILE_FOLDER, `error.${filename}.log`),
                     level: 'error',
                     datePattern: 'YYYY-MM-DD', 
                     zippedArchive: true,
                     maxSize: '10m', 
                     maxFiles: '10d'  
                    })
            ],
        }); 
    }
      

    logger() {
        return this._logger;
    }
}



let applicationLogger;  // Variable to hold a singleton instance of the logger.

/**
 * @function initializeLogger
 * @description Initializes the logger with the specified filename. This is not exported and is used internally to initialize the logger.
 * @param {string} filename - The name of the file to log to. Log file will be stored in the folder specified in the LOG_FILE_FOLDER environment variable.
 */
export function initializeLogger(filename) {
    console.log("Initializing logger for " + filename);
    applicationLogger = new WinstonLogger(filename);
}

/**
 * @function getLogger
 * @description Returns a logger instance for the specified module. 
 * This method creates a singleton instance of the logger when it is called the first time in the application.
 * Modules should call this method to get access to the application wide logger.
 * 
 * @param {string} callingModule - The name of the module that is calling this function.
 * @returns {winston.Logger} A logger instance for the specified module.
 */
export function getLogger(callingModule) {
    // The calling function passes the `meta.url` property with the file path as the value.
    // We need to extract the last part of the path as the module name.
  const getLabel = (numParts) => {
        console.log(callingModule)
        const parts = callingModule.split("/");
        const label = parts.slice(-numParts).join("/");
        return label;
    }

    
    // If the logger is not initialized, initialize it with the module name.
    // This is not ideal and the assumption is that the method will be called first from the main entry point of the application.
    // The module name would be the last part of the file path of the entry point.
    if(!applicationLogger) {
        initializeLogger(getLabel(1));
    }
    
    // Return a logger instance for the specified module.
    // logger.child returns a new logger that has all the configurations of the parent logger
    // but also prints the module name as an additional property in the log message.
    return applicationLogger.logger().child({module: getLabel(2)});
}
