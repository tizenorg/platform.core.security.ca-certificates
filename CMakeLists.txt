CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

SET(PATH_CRT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/ca-bundle.pem")

MESSAGE("Generate ca-bundle.pem file")

EXECUTE_PROCESS(
	COMMAND
	${CMAKE_CURRENT_SOURCE_DIR}/concat-cacerts.sh
	${CMAKE_CURRENT_SOURCE_DIR}/certs
	${PATH_CRT_FILE}
	RESULT_VARIABLE ERROR_CODE
)

IF(ERROR_CODE)
	MESSAGE(FATAL_ERROR "Failed to generate ca-bundle.pem file")
ENDIF(ERROR_CODE)

INSTALL(FILES
	${PATH_CRT_FILE}
	DESTINATION /var/lib/ca-certificates
)

CONFIGURE_FILE(packaging/ca-certificates.manifest.in ca-certificates.manifest @ONLY)
