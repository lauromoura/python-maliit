project(pymaliit)

set(maliit_SRC
    ${CMAKE_CURRENT_BINARY_DIR}/maliit/maliit_module_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/maliit/maliit_python.h
    ${CMAKE_CURRENT_BINARY_DIR}/maliit/maliit_attributeextension_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/maliit/maliit_inputmethod_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/maliit/maliit_inputmethodquery_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/maliit/maliit_preeditinjectionevent_wrapper.cpp
)

set(MALIIT_INCLUDE_DIRS_FIX "")
foreach(LOOP_FIX ${MALIIT_INCLUDE_DIRS})
    message(STATUS "${MALIIT_INCLUDE_DIRS_FIX}")
    list(APPEND MALIIT_INCLUDE_DIRS_FIX "${LOOP_FIX}/maliit")
endforeach(LOOP_FIX)

set(maliit_INCLUDE_DIRECTORIES
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${SHIBOKEN_INCLUDE_DIR}
    ${SHIBOKEN_PYTHON_INCLUDE_DIR}
    ${PYTHON_INCLUDE_PATH}
    ${PYSIDE_INCLUDE_DIR}
    ${PYSIDE_INCLUDE_DIR}/QtCore
    ${QT_INCLUDE_DIR}
    ${QT_QTCORE_INCLUDE_DIR}
    ${QT_QTGUI_INCLUDE_DIR}
    ${MALIIT_INCLUDE_DIRS_FIX}
    ${MALIIT_PLUGINS_INCLUDE_DIRS}
)

set(maliit_LINK_LIBRARIES
    ${SHIBOKEN_PYTHON_LIBRARIES}
    ${SHIBOKEN_LIBRARY}
    ${QT_QTCORE_LIBRARY}
    ${QT_QTGUI_LIBRARY}
    ${PYSIDE_LIBRARY}
    ${MALIIT_LIBRARIES}
    ${MALIIT_PLUGINS_LIBRARIES}
)

set(MALIIT_INCLUDE_DIRS_FIX_COLON "")
foreach(LOOP_FIX_COLON ${MALIIT_INCLUDE_DIRS})
    set(MALIIT_INCLUDE_DIRS_FIX_COLON "${MALIIT_INCLUDE_DIRS_FIX_COLON}:${LOOP_FIX_COLON}")
endforeach(LOOP_FIX_COLON)

link_directories(${MALIIT_LIBRARY_DIRS})
include_directories(maliit ${maliit_INCLUDE_DIRECTORIES})
add_library(maliit MODULE ${maliit_SRC})
set_property(TARGET maliit PROPERTY PREFIX "")
target_link_libraries(maliit ${maliit_LINK_LIBRARIES})

add_custom_command(OUTPUT ${maliit_SRC}
                   COMMAND ${GENERATORRUNNER_BINARY}
                   --generatorSet=shiboken --enable-parent-ctor-heuristic --enable-pyside-extensions --enable-return-value-heuristic
                   ${CMAKE_CURRENT_SOURCE_DIR}/global.h
                   --include-paths=${QT_INCLUDE_DIR}:${MALIIT_INCLUDE_DIRS_FIX_COLON}
                   --typesystem-paths=${typesystem_path}:${PYSIDE_TYPESYSTEMS}
                   --output-directory=${CMAKE_CURRENT_BINARY_DIR}
                   --api-version="maliit*,${MALIIT_VERSION}|PySide*,${QT_VERSION_MAJOR}.${QT_VERSION_MINOR}"
                   ${CMAKE_CURRENT_SOURCE_DIR}/typesystem_maliit.xml
                   WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                   COMMENT "Running generator for maliit..."
                  )

install(TARGETS maliit
        LIBRARY DESTINATION ${SITE_PACKAGE})

