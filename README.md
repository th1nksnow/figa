## Архитектура
                      
                 https://web.thinksnow.ru              
                            │                       
                            │                  
                            │                         
                    ┌───────▼───────┐                 
                    │ INGRESS NGINX │                 
                    └───────┬───────┘                    
                            │           
                            │  
                            │                                  
                        HTTP│    
                            │   
         get history ┌──────▼─────┐ figalize                 
           ┌─────────┤  FRONTEND  ├───────────┐          
           │         └────────────┘ get schema│              
           │                                  │             
           │                                  │           
    ┌──────▼────────┐                ┌────────▼─────┐  
    │ HISTORY, PULL │  POST history  │   FIGALIZE   │  
    │ microservices │◄───────────────┤ microservice │ 
    └──────┬────────┘                └──────────────┘ 
           │                              
           │                         
           │       ┌──────────┐         
           │       │          │        
           │STORE  │          │        
           └──────►│POSTGRESQL│
            QUERY  │          │
                   │          │
                   └──────────┘
