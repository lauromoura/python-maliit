project(pymaliit)

set(plugins080_SRC
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/mabstractinputmethod_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/mabstractinputmethod_wrapper.h
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/mabstractinputmethodhost_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/mabstractinputmethodhost_wrapper.h
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/mabstractinputmethodsettings_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/mabstractinputmethodsettings_wrapper.h
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/plugins080_module_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/plugins080_python.h
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/mimplugindescription_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/mimplugindescription_wrapper.h
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/minputmethod_preedittextformat_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/minputmethod_preedittextformat_wrapper.h
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/minputmethod_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/minputmethod_wrapper.h
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/minputmethodplugin_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/plugins080/minputmethodplugin_wrapper.h
)

set(plugins080_INCLUDE_DIRECTORIES
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${SHIBOKEN_INCLUDE_DIR}
    ${SHIBOKEN_PYTHON_INCLUDE_DIR}
    ${PYTHON_INCLUDE_PATH}
    ${PYSIDE_INCLUDE_DIR}
    ${PYSIDE_INCLUDE_DIR}/QtCore
    ${PYSIDE_INCLUDE_DIR}/QtGui
    ${QT_INCLUDE_DIR}
    ${QT_QTCORE_INCLUDE_DIR}
    ${QT_QTGUI_INCLUDE_DIR}
    ${MALIIT_INCLUDE_DIRS}
    ${MALIIT_PLUGINS_INCLUDE_DIRS}
)

set(plugins080_LINK_LIBRARIES
    ${SHIBOKEN_PYTHON_LIBRARIES}
    ${SHIBOKEN_LIBRARY}
    ${QT_QTCORE_LIBRARY}
    ${QT_QTGUI_LIBRARY}
    ${PYSIDE_LIBRARY}
    ${MALIIT_LIBRARIES}
    ${MALIIT_PLUGINS_LIBRARIES}
)

set(MALIIT_PLUGINS_INCLUDE_DIRS_FIX "")
foreach(LOOP_FIX ${MALIIT_PLUGINS_INCLUDE_DIRS})
    set(MALIIT_PLUGINS_INCLUDE_DIRS_FIX "${MALIIT_PLUGINS_INCLUDE_DIRS_FIX}:${LOOP_FIX}")
endforeach(LOOP_FIX)

link_directories(${MALIIT_LIBRARY_DIRS})
include_directories(plugins080 ${plugins080_INCLUDE_DIRECTORIES})
add_library(plugins080 MODULE ${plugins080_SRC})
set_property(TARGET plugins080 PROPERTY PREFIX "")
target_link_libraries(plugins080 ${plugins080_LINK_LIBRARIES})

add_custom_command(OUTPUT ${plugins080_SRC}
                   COMMAND ${GENERATORRUNNER_BINARY}
                   --generatorSet=shiboken --enable-parent-ctor-heuristic --enable-pyside-extensions --enable-return-value-heuristic
                   ${CMAKE_CURRENT_SOURCE_DIR}/global.h
                   --include-paths=${QT_INCLUDE_DIR}:${MALIIT_PLUGINS_INCLUDE_DIRS_FIX}
                   --typesystem-paths=${typesystem_path}:${PYSIDE_TYPESYSTEMS}
                   --output-directory=${CMAKE_CURRENT_BINARY_DIR}
                   --api-version="plugins080*,${MALIIT_VERSION}|PySide*,${QT_VERSION_MAJOR}.${QT_VERSION_MINOR}"
                   ${CMAKE_CURRENT_SOURCE_DIR}/typesystem_maliit.xml
                   WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                   COMMENT "Running generator for plugins080..."
                  )

install(TARGETS plugins080
        LIBRARY DESTINATION ${SITE_PACKAGE}/maliit/plugins/)

