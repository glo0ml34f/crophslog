-- Fetch user ID from GET params
      local user_id = HTTP_GET_PARAM_BY_NAME("id")
      local sanitized_id = sanitize_input(user_id)

-- Query user info based on sanitized ID
        local query = "SELECT * FROM users WHERE id = " .. sanitized_id
        local result = db_query(query)
        OUT(result)

-- Multi-line block with internal logic
        local sys_info = {}
        sys_info.uptime = io.popen("uptime"):read("*a")
        sys_info.memory = io.popen("free -m"):read("*a")
        
        for k, v in pairs(sys_info) do
          print(k .. ": " .. v)
        end

-- Footer block
        print("Dashboard generated at: " .. os.date())