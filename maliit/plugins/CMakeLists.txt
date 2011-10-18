project(plugins)

# TODO Conditional compilation based on available plugins version
# Must update maliit detection too
add_subdirectory(plugins080)

install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/__init__.py"
    DESTINATION "${SITE_PACKAGE}/maliit/plugins/")
