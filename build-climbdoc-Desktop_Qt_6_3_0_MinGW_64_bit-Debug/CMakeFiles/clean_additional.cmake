# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles\\climbdoc_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\climbdoc_autogen.dir\\ParseCache.txt"
  "climbdoc_autogen"
  )
endif()
