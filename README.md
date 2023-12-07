## Архитектура
                      
                 https://figachechnaya.ru              
                            │                       
                            │SSL                  
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
    │    HISTORY    │  POST history  │   FIGALIZE   │  
    │  microservice │◄───────────────┤ microservice │ 
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
