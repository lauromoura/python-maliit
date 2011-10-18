project(pymaliit)

add_subdirectory(client)
add_subdirectory(plugins)

install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/__init__.py"
    DESTINATION "${SITE_PACKAGE}/maliit/")
