server <- function(input, output){
  selected_data <- reactive({
    # Connect to the DB
    conn <- dbConnect(
      RPostgres::Postgres(),
      dbname = "mwkim",
      host = "172.28.0.3",
      port = "5432",
      user = "mwkim",
      password = "mwkim"
    )
    
    # Get the data (컬럼명 소문자로 변경)
    corona <- dbGetQuery(conn, glue("
      SELECT 
        to_date(substring(s_dt,1,10),'YYYY.MM.DD') as s_dt,
        n_hj::float as n_hj,
        t_hj as t_hj
      FROM tbcorona19countstatus_bulk2
      WHERE to_date(substring(s_dt,1,10),'YYYY.MM.DD') 
        BETWEEN '{format(input$dates[1])}' AND '{format(input$dates[2])}'
    "))
    
    # Disconnect from the DB
    dbDisconnect(conn)
    
    # Convert to data.frame
    data.frame(corona)
  })
  
  output$daily_confirmed <- renderPlot({
    ggplot(data=selected_data(), aes(x=s_dt, y=n_hj)) + 
      geom_line(color='blue', linewidth = 1) + 
      geom_point(color='red') + 
      geom_smooth(method='lm') +
      ggtitle("Daily confirmed cases") +
      labs(x='Date',y='Daily confirmed cases')
  })
  
  output$total_confirmed <- renderPlot({
    ggplot(data=selected_data(), aes(x=s_dt, y=t_hj)) +
      geom_line(color='blue', linewidth = 1) +
      geom_point(color='red') +
      geom_smooth(method='lm') +
      ggtitle("Total confirmed cases") +
      labs(x='Date',y='Total confirmed cases')
  })
}
