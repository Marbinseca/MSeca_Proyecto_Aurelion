import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import mysql.connector
import warnings
warnings.filterwarnings('ignore')

# Paleta de colores profesional moderna
COLOR_PALETTE = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#6B8E23']
BACKGROUND_COLOR = '#f8f9fa'
CARD_BACKGROUND = '#ffffff'
TEXT_COLOR = '#2c3e50'
ACCENT_COLOR = '#3498db'

# Coordenadas de las ciudades de Córdoba (aproximadas)
COORDENADAS_CIUDADES = {
    'Cordoba': {'lat': -31.4201, 'lon': -64.1888},
    'Carlos Paz': {'lat': -31.4248, 'lon': -64.4977},
    'Rio Cuarto': {'lat': -33.1230, 'lon': -64.3478},
    'Villa Maria': {'lat': -32.4105, 'lon': -63.2436},
    'Alta Gracia': {'lat': -31.6583, 'lon': -64.4285},
    'Mendiolaza': {'lat': -31.2675, 'lon': -64.3000}
}

# Conexión a la base de datos
def conectar_bd():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'AurelionDB',
        'port': 3306
    }
    return mysql.connector.connect(**config)

# Obtener datos para el dashboard
def obtener_datos_dashboard():
    conn = conectar_bd()
    
    query = """
    SELECT 
        v.id_venta,
        v.fecha,
        v.id_cliente,
        v.medio_pago,
        c.ciudad,
        c.nombre_cliente,
        dv.id_producto,
        dv.nombre_producto,
        dv.cantidad,
        dv.precio_unitario,
        dv.importe,
        p.categoria
    FROM Ventas v
    JOIN Clientes c ON v.id_cliente = c.id_cliente
    JOIN Detalles_Ventas dv ON v.id_venta = dv.id_venta
    JOIN Productos p ON dv.id_producto = p.id_producto
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Procesamiento de datos
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month_name()
    df['dia_semana'] = df['fecha'].dt.day_name()
    df['trimestre'] = df['fecha'].dt.quarter
    
    return df

# Cargar datos
df = obtener_datos_dashboard()

# Inicializar la app Dash CON LA SOLUCIÓN DEL ERROR
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Titulo de la pestaña
app.title = "Aurelion Analytics - Business Intelligence"
# Opcional: Si quieres usar un favicon de URL externa
html.Link(
    rel='icon',
    href='https://cdn-icons-png.flaticon.com/256/1828/1828533.png'
)

# Layout del dashboard profesional con pestañas
app.layout = html.Div([
    # Header con logo y título
    html.Div([
        html.Div([
            html.H1("AURELION ANALYTICS", 
                   style={
                       'color': TEXT_COLOR, 
                       'margin': 0,
                       'fontSize': '28px',
                       'fontWeight': '700',
                       'letterSpacing': '1px'
                   }),
            
            html.P("Business Intelligence Dashboard", 
                  style={
                      'color': '#7f8c8d',
                      'margin': 0,
                      'fontSize': '14px',
                      'fontWeight': '300'
                  }),
        ], style={'textAlign': 'center', 'padding': '20px 0'})
    ], style={
        'backgroundColor': CARD_BACKGROUND,
        'borderBottom': f'3px solid {ACCENT_COLOR}',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
        'marginBottom': '30px'
    }),
    
    # Pestañas
    dcc.Tabs(id="tabs-analytics", value='tab-analytics', children=[
        dcc.Tab(label='📊 ANÁLISIS COMERCIAL', value='tab-analytics', 
                style={'fontWeight': '600', 'padding': '10px'},
                selected_style={'backgroundColor': ACCENT_COLOR, 'color': 'white'}),
        dcc.Tab(label='🗺️ GEOANALÍTICA', value='tab-geo', 
                style={'fontWeight': '600', 'padding': '10px'},
                selected_style={'backgroundColor': ACCENT_COLOR, 'color': 'white'}),
    ], style={'marginBottom': '20px'}),
    
    # Contenido de las pestañas
    html.Div(id='tabs-content'), 
    
    html.Div([
        html.Hr(style={'margin': '40px 0 20px 0'}),
        html.P("© 2025 Aurelion Analytics - Business Intelligence Platform", 
              style={
                  'textAlign': 'center',
                  'color': '#95a5a6',
                  'fontSize': '12px',
                  'margin': '20px 0',
                  'fontWeight': '300'
              })
    ], style={
        'marginTop': '50px'
    })
    
], style={
    'backgroundColor': BACKGROUND_COLOR,
    'padding': '20px',
    'minHeight': '100vh',
    'fontFamily': 'Inter, sans-serif'
    
    
})

# Callback para cambiar entre pestañas
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs-analytics', 'value')]
)
def render_content(tab):
    if tab == 'tab-analytics':
        return html.Div([
            # Filtros en tarjeta elegante
            html.Div([
                html.Div([
                    html.H3("FILTROS", 
                           style={
                               'color': TEXT_COLOR,
                               'marginBottom': '20px',
                               'fontSize': '16px',
                               'fontWeight': '600',
                               'borderBottom': f'2px solid {ACCENT_COLOR}',
                               'paddingBottom': '10px'
                           }),
                    
                    # Filtros en fila horizontal
                    html.Div([
                        # Filtro de Ciudad - 50%
                        html.Div([
                            html.Label("CIUDAD", 
                                      style={
                                          'fontWeight': '500',
                                          'color': TEXT_COLOR,
                                          'marginBottom': '8px',
                                          'fontSize': '12px',
                                          'textTransform': 'uppercase',
                                          'letterSpacing': '0.5px'
                                      }),
                            dcc.Dropdown(
                                id='ciudad-filter',
                                options=[{'label': 'Todas las Ciudades', 'value': 'all'}] + 
                                        [{'label': ciudad, 'value': ciudad} for ciudad in sorted(df['ciudad'].unique())],
                                value='all',
                                style={'width': '100%'}
                            )
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '2%'}),
                        
                        # Filtro de Categoría - 50%
                        html.Div([
                            html.Label("CATEGORÍA", 
                                      style={
                                          'fontWeight': '500',
                                          'color': TEXT_COLOR,
                                          'marginBottom': '8px',
                                          'fontSize': '12px',
                                          'textTransform': 'uppercase',
                                          'letterSpacing': '0.5px'
                                      }),
                            dcc.Dropdown(
                                id='categoria-filter',
                                options=[{'label': 'Todas las Categorías', 'value': 'all'}] + 
                                        [{'label': cat, 'value': cat} for cat in sorted(df['categoria'].unique())],
                                value='all',
                                style={'width': '100%'}
                            )
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '2%'}),
                    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'})
                ], style={
                    'backgroundColor': CARD_BACKGROUND,
                    'padding': '25px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                    'marginBottom': '30px'
                })
            ]),
            
            
            # KPIs en tarjeta elegante
            html.Div([
                html.Div([
                    html.H3("📊 MÉTRICAS PRINCIPALES", 
                           style={
                               'color': TEXT_COLOR,
                               'marginBottom': '20px',
                               'fontSize': '18px',
                               'fontWeight': '600',
                               'borderBottom': f'2px solid {ACCENT_COLOR}',
                               'paddingBottom': '10px'
                           }),
                    
                    html.Div([
                        # KPI 1: Ingresos Totales
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-dollar-sign", 
                                      style={'color': COLOR_PALETTE[0], 'fontSize': '24px', 'marginBottom': '10px'}),
                                html.H4("Ingresos Totales", 
                                       style={'color': TEXT_COLOR, 'margin': '5px 0', 'fontSize': '14px', 'fontWeight': '500'}),
                                html.H3(id='kpi-ingresos',
                                       style={'color': COLOR_PALETTE[0], 'margin': '0', 'fontSize': '24px', 'fontWeight': '700'})
                            ], style={'textAlign': 'center', 'padding': '20px'})
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'borderRadius': '8px',
                            'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                            'flex': '1',
                            'margin': '0 10px'
                        }),
                        
                        # KPI 2: Total Ventas
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-shopping-cart", 
                                      style={'color': COLOR_PALETTE[1], 'fontSize': '24px', 'marginBottom': '10px'}),
                                html.H4("Total Ventas", 
                                       style={'color': TEXT_COLOR, 'margin': '5px 0', 'fontSize': '14px', 'fontWeight': '500'}),
                                html.H3(id='kpi-ventas',
                                       style={'color': COLOR_PALETTE[1], 'margin': '0', 'fontSize': '24px', 'fontWeight': '700'})
                            ], style={'textAlign': 'center', 'padding': '20px'})
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'borderRadius': '8px',
                            'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                            'flex': '1',
                            'margin': '0 10px'
                        }),
                        
                        # KPI 3: Clientes Únicos
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-users", 
                                      style={'color': COLOR_PALETTE[2], 'fontSize': '24px', 'marginBottom': '10px'}),
                                html.H4("Clientes Únicos", 
                                       style={'color': TEXT_COLOR, 'margin': '5px 0', 'fontSize': '14px', 'fontWeight': '500'}),
                                html.H3(id='kpi-clientes',
                                       style={'color': COLOR_PALETTE[2], 'margin': '0', 'fontSize': '24px', 'fontWeight': '700'})
                            ], style={'textAlign': 'center', 'padding': '20px'})
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'borderRadius': '8px',
                            'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                            'flex': '1',
                            'margin': '0 10px'
                        }),
                        
                        # KPI 4: Productos Vendidos
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-box", 
                                      style={'color': COLOR_PALETTE[3], 'fontSize': '24px', 'marginBottom': '10px'}),
                                html.H4("Productos Vendidos", 
                                       style={'color': TEXT_COLOR, 'margin': '5px 0', 'fontSize': '14px', 'fontWeight': '500'}),
                                html.H3(id='kpi-productos',
                                       style={'color': COLOR_PALETTE[3], 'margin': '0', 'fontSize': '24px', 'fontWeight': '700'})
                            ], style={'textAlign': 'center', 'padding': '20px'})
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'borderRadius': '8px',
                            'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                            'flex': '1',
                            'margin': '0 10px'
                        }),
                        
                        # KPI 5: Ticket Promedio
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-receipt", 
                                      style={'color': COLOR_PALETTE[4], 'fontSize': '24px', 'marginBottom': '10px'}),
                                html.H4("Ticket Promedio", 
                                       style={'color': TEXT_COLOR, 'margin': '5px 0', 'fontSize': '14px', 'fontWeight': '500'}),
                                html.H3(id='kpi-ticket',
                                       style={'color': COLOR_PALETTE[4], 'margin': '0', 'fontSize': '24px', 'fontWeight': '700'})
                            ], style={'textAlign': 'center', 'padding': '20px'})
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'borderRadius': '8px',
                            'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                            'flex': '1',
                            'margin': '0 10px'
                        })
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'flexWrap': 'wrap'})
                ], style={
                    'backgroundColor': CARD_BACKGROUND,
                    'padding': '25px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                    'marginBottom': '30px'
                })
            ]),      
            
            
            # Gráficos de análisis comercial
            html.Div([
                # Fila 1: Gráficos grandes
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3([
                                html.I(className="fas fa-chart-line", style={'marginRight': '10px'}),
                                "ANÁLISIS PARETO - PRODUCTOS CLAVE"
                            ], style={
                                'color': TEXT_COLOR,
                                'marginBottom': '15px',
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'borderBottom': f'2px solid {COLOR_PALETTE[0]}',
                                'paddingBottom': '10px'
                            }),
                            dcc.Graph(id='grafico-pareto')
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'padding': '25px',
                            'borderRadius': '12px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                            'height': '100%'
                        })
                    ], className='twelve columns', style={'marginBottom': '25px'}),
                ], className='row'),
                
                # Fila 2: Gráficos medianos
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3([
                                html.I(className="fas fa-city", style={'marginRight': '10px'}),
                                "RENTABILIDAD POR CIUDAD"
                            ], style={
                                'color': TEXT_COLOR,
                                'marginBottom': '15px',
                                'fontSize': '16px',
                                'fontWeight': '600'
                            }),
                            dcc.Graph(id='grafico-ciudades')
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'padding': '20px',
                            'borderRadius': '12px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                            'height': '100%'
                        })
                    ], className='six columns', style={'marginBottom': '25px', 'padding': '0 10px'}),
                    
                    html.Div([
                        html.Div([
                            html.H3([
                                html.I(className="fas fa-credit-card", style={'marginRight': '10px'}),
                                "PREFERENCIA DE PAGO"
                            ], style={
                                'color': TEXT_COLOR,
                                'marginBottom': '15px',
                                'fontSize': '16px',
                                'fontWeight': '600'
                            }),
                            dcc.Graph(id='grafico-medios-pago')
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'padding': '20px',
                            'borderRadius': '12px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                            'height': '100%'
                        })
                    ], className='six columns', style={'marginBottom': '25px', 'padding': '0 10px'}),
                ], className='row'),
                
                # Fila 3: Gráficos medianos
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3([
                                html.I(className="fas fa-calendar-alt", style={'marginRight': '10px'}),
                                "PATRÓN SEMANAL DE VENTAS"
                            ], style={
                                'color': TEXT_COLOR,
                                'marginBottom': '15px',
                                'fontSize': '16px',
                                'fontWeight': '600'
                            }),
                            dcc.Graph(id='grafico-dias-semana')
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'padding': '20px',
                            'borderRadius': '12px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                            'height': '100%'
                        })
                    ], className='six columns', style={'marginBottom': '25px', 'padding': '0 10px'}),
                    
                    html.Div([
                        html.Div([
                            html.H3([
                                html.I(className="fas fa-receipt", style={'marginRight': '10px'}),
                                "TICKET PROMEDIO"
                            ], style={
                                'color': TEXT_COLOR,
                                'marginBottom': '15px',
                                'fontSize': '16px',
                                'fontWeight': '600'
                            }),
                            dcc.Graph(id='grafico-ticket-promedio')
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'padding': '20px',
                            'borderRadius': '12px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                            'height': '100%'
                        })
                    ], className='six columns', style={'marginBottom': '25px', 'padding': '0 10px'}),
                ], className='row'),
                
                # Fila 4: Gráfico grande final
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3([
                                html.I(className="fas fa-users", style={'marginRight': '10px'}),
                                "CLIENTES DE ALTO VALOR"
                            ], style={
                                'color': TEXT_COLOR,
                                'marginBottom': '15px',
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'borderBottom': f'2px solid {COLOR_PALETTE[4]}',
                                'paddingBottom': '10px'
                            }),
                            dcc.Graph(id='grafico-clientes-top')
                        ], style={
                            'backgroundColor': CARD_BACKGROUND,
                            'padding': '25px',
                            'borderRadius': '12px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                            'height': '100%'
                        })
                    ], className='twelve columns', style={'marginBottom': '25px'}),
                ], className='row'),
                
            ])
        ])
    
    elif tab == 'tab-geo':
        return html.Div([
            # Filtros para geoanalítica
            html.Div([
                html.Div([
                    html.H3("FILTROS GEOANALÍTICA", 
                           style={
                               'color': TEXT_COLOR,
                               'marginBottom': '20px',
                               'fontSize': '16px',
                               'fontWeight': '600',
                               'borderBottom': f'2px solid {ACCENT_COLOR}',
                               'paddingBottom': '10px'
                           }),
                    
                    html.Div([
                        html.Div([
                            html.Label("MÉTRICA A VISUALIZAR", 
                                      style={
                                          'fontWeight': '500',
                                          'color': TEXT_COLOR,
                                          'marginBottom': '8px',
                                          'fontSize': '12px',
                                          'textTransform': 'uppercase',
                                          'letterSpacing': '0.5px'
                                      }),
                            dcc.Dropdown(
                                id='metrica-geo',
                                options=[
                                    {'label': 'Ingresos Totales', 'value': 'ingresos'},
                                    {'label': 'Número de Ventas', 'value': 'ventas'},
                                    {'label': 'Ticket Promedio', 'value': 'ticket'},
                                    {'label': 'Clientes Únicos', 'value': 'clientes'}
                                ],
                                value='ingresos',
                                style={'width': '100%'}
                            )
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '2%'}),
                        
                        html.Div([
                            html.Label("TAMAÑO DE BURBUJA", 
                                      style={
                                          'fontWeight': '500',
                                          'color': TEXT_COLOR,
                                          'marginBottom': '8px',
                                          'fontSize': '12px',
                                          'textTransform': 'uppercase',
                                          'letterSpacing': '0.5px'
                                      }),
                            dcc.Slider(
                                id='size-slider',
                                min=10,
                                max=50,
                                step=5,
                                value=25,
                                marks={i: str(i) for i in range(10, 51, 10)}
                            )
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '2%'}),
                    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'})
                ], style={
                    'backgroundColor': CARD_BACKGROUND,
                    'padding': '25px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                    'marginBottom': '30px'
                })
            ]),
            
            # Mapa y métricas
            html.Div([
                html.Div([
                    html.Div([
                        html.H3([
                            html.I(className="fas fa-map-marked-alt", style={'marginRight': '10px'}),
                            "MAPA DE CALOR GEOGRÁFICO"
                        ], style={
                            'color': TEXT_COLOR,
                            'marginBottom': '15px',
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'borderBottom': f'2px solid {COLOR_PALETTE[1]}',
                            'paddingBottom': '10px'
                        }),
                        dcc.Graph(id='mapa-geografico')
                    ], style={
                        'backgroundColor': CARD_BACKGROUND,
                        'padding': '25px',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                        'height': '100%'
                    })
                ], className='eight columns', style={'marginBottom': '25px', 'padding': '0 10px'}),
                
                html.Div([
                    html.Div([
                        html.H3([
                            html.I(className="fas fa-chart-bar", style={'marginRight': '10px'}),
                            "MÉTRICAS POR CIUDAD"
                        ], style={
                            'color': TEXT_COLOR,
                            'marginBottom': '15px',
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'borderBottom': f'2px solid {COLOR_PALETTE[2]}',
                            'paddingBottom': '10px'
                        }),
                        dcc.Graph(id='metricas-ciudades')
                    ], style={
                        'backgroundColor': CARD_BACKGROUND,
                        'padding': '25px',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                        'height': '100%'
                    })
                ], className='four columns', style={'marginBottom': '25px', 'padding': '0 10px'}),
            ], className='row'),
            
            # Gráficos adicionales de geoanalítica
            html.Div([
                html.Div([
                    html.Div([
                        html.H3([
                            html.I(className="fas fa-chart-pie", style={'marginRight': '10px'}),
                            "DISTRIBUCIÓN REGIONAL"
                        ], style={
                            'color': TEXT_COLOR,
                            'marginBottom': '15px',
                            'fontSize': '16px',
                            'fontWeight': '600'
                        }),
                        dcc.Graph(id='distribucion-regional')
                    ], style={
                        'backgroundColor': CARD_BACKGROUND,
                        'padding': '20px',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                        'height': '100%'
                    })
                ], className='six columns', style={'marginBottom': '25px', 'padding': '0 10px'}),
                
                html.Div([
                    html.Div([
                        html.H3([
                            html.I(className="fas fa-trending-up", style={'marginRight': '10px'}),
                            "CRECIMIENTO POR CIUDAD"
                        ], style={
                            'color': TEXT_COLOR,
                            'marginBottom': '15px',
                            'fontSize': '16px',
                            'fontWeight': '600'
                        }),
                        dcc.Graph(id='crecimiento-ciudades')
                    ], style={
                        'backgroundColor': CARD_BACKGROUND,
                        'padding': '20px',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
                        'height': '100%'
                    })
                ], className='six columns', style={'marginBottom': '25px', 'padding': '0 10px'}),
            ], className='row')
            
        ])

# Callbacks para los filtros del análisis comercial
@app.callback(
    [Output('grafico-pareto', 'figure'),
     Output('grafico-ciudades', 'figure'),
     Output('grafico-medios-pago', 'figure'),
     Output('grafico-dias-semana', 'figure'),
     Output('grafico-ticket-promedio', 'figure'),
     Output('grafico-clientes-top', 'figure')],
    [Input('ciudad-filter', 'value'),
     Input('categoria-filter', 'value')]
)
def update_dashboard(ciudad_seleccionada, categoria_seleccionada):
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if ciudad_seleccionada != 'all':
        df_filtrado = df_filtrado[df_filtrado['ciudad'] == ciudad_seleccionada]
    
    if categoria_seleccionada != 'all':
        df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_seleccionada]
    
    # 1. Gráfico Pareto - Productos que generan el 80% de ingresos
    ingresos_productos = df_filtrado.groupby('nombre_producto')['importe'].sum().sort_values(ascending=False)
    ingresos_productos_cumsum = ingresos_productos.cumsum()
    total_ingresos = ingresos_productos.sum()
    limite_80 = total_ingresos * 0.8
    
    fig_pareto = go.Figure()
    
    fig_pareto.add_trace(go.Bar(
        x=ingresos_productos.index,
        y=ingresos_productos.values,
        name='Ingresos por Producto',
        marker_color=COLOR_PALETTE[0],
        marker_line_width=0
    ))
    
    fig_pareto.add_trace(go.Scatter(
        x=ingresos_productos.index,
        y=ingresos_productos_cumsum.values,
        name='Acumulado',
        yaxis='y2',
        line=dict(color=COLOR_PALETTE[1], width=3),
        marker=dict(size=6)
    ))
    
    fig_pareto.add_hline(y=limite_80, line_dash="dash", line_color="red", 
                        annotation_text="80% del Total", annotation_font_size=12)
    
    fig_pareto.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR),
        title=dict(
            text='Distribución de Ingresos por Producto',
            x=0.5,
            font=dict(size=16, color=TEXT_COLOR)
        ),
        xaxis=dict(
            showgrid=False,
            tickangle=45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#ecf0f1',
            title='Ingresos ($)'
        ),
        yaxis2=dict(
            title='Ingresos Acumulados ($)', 
            overlaying='y', 
            side='right',
            showgrid=False
        ),
        showlegend=True,
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # 2. Gráfico Ciudades Más Rentables
    ingresos_ciudad = df_filtrado.groupby('ciudad')['importe'].sum().sort_values(ascending=False)
    
    fig_ciudades = px.bar(
        x=ingresos_ciudad.index,
        y=ingresos_ciudad.values,
        title='Ingresos Totales por Ciudad',
        labels={'x': 'Ciudad', 'y': 'Ingresos Totales ($)'},
        color=ingresos_ciudad.values,
        color_continuous_scale=[COLOR_PALETTE[0], COLOR_PALETTE[2]]
    )
    
    fig_ciudades.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
    )
    
    # 3. Gráfico Medios de Pago
    medios_pago = df_filtrado.groupby('medio_pago')['importe'].sum().sort_values(ascending=False)
    
    fig_medios_pago = px.pie(
        values=medios_pago.values,
        names=medios_pago.index,
        title='Distribución por Medio de Pago',
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig_medios_pago.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1
        )
    )
    
    # 4. Gráfico Días de la Semana
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    nombres_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    ventas_dias = df_filtrado.groupby('dia_semana')['importe'].sum().reindex(dias_orden)
    
    fig_dias_semana = px.bar(
        x=nombres_espanol,
        y=ventas_dias.values,
        title='Ventas por Día de la Semana',
        labels={'x': 'Día de la Semana', 'y': 'Ingresos Totales ($)'},
        color=ventas_dias.values,
        color_continuous_scale=[COLOR_PALETTE[3], COLOR_PALETTE[4]]
    )
    
    fig_dias_semana.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
    )
    
    # 5. Gráfico Ticket Promedio por Ciudad
    ticket_promedio = df_filtrado.groupby('ciudad')['importe'].mean().sort_values(ascending=False)
    
    fig_ticket_promedio = px.bar(
        x=ticket_promedio.index,
        y=ticket_promedio.values,
        title='Ticket Promedio por Ciudad',
        labels={'x': 'Ciudad', 'y': 'Ticket Promedio ($)'},
        color=ticket_promedio.values,
        color_continuous_scale=[COLOR_PALETTE[5], COLOR_PALETTE[1]]
    )
    
    fig_ticket_promedio.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
    )
    
    # 6. Gráfico Clientes Más Valiosos (Top 10)
    clientes_top = df_filtrado.groupby('nombre_cliente')['importe'].sum().nlargest(10).sort_values(ascending=True)
    
    fig_clientes_top = px.bar(
        y=clientes_top.index,
        x=clientes_top.values,
        title='Top 10 Clientes por Valor',
        labels={'x': 'Ingresos Totales ($)', 'y': 'Cliente'},
        orientation='h',
        color=clientes_top.values,
        color_continuous_scale=[COLOR_PALETTE[0], COLOR_PALETTE[2]]
    )
    
    fig_clientes_top.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR),
        showlegend=False,
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=True, gridcolor='#ecf0f1')
    )
    
    return fig_pareto, fig_ciudades, fig_medios_pago, fig_dias_semana, fig_ticket_promedio, fig_clientes_top


# Callback para los KPIs dinámicos
@app.callback(
    [Output('kpi-ingresos', 'children'),
     Output('kpi-ventas', 'children'),
     Output('kpi-clientes', 'children'),
     Output('kpi-productos', 'children'),
     Output('kpi-ticket', 'children')],
    [Input('ciudad-filter', 'value'),
     Input('categoria-filter', 'value')]
)
def update_kpis(ciudad_seleccionada, categoria_seleccionada):
    # Aplicar filtros al DataFrame
    df_filtrado = df.copy()
    
    if ciudad_seleccionada != 'all':
        df_filtrado = df_filtrado[df_filtrado['ciudad'] == ciudad_seleccionada]
    
    if categoria_seleccionada != 'all':
        df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_seleccionada]
    
    # Calcular métricas filtradas
    ingresos_totales = df_filtrado['importe'].sum()
    total_ventas = df_filtrado['id_venta'].nunique()
    
    # Clientes únicos - CONSULTA FILTRADA A TABLAS ORIGINALES
    conn = conectar_bd()
    
    # Construir consulta de clientes con filtros
    query_clientes = """
    SELECT COUNT(DISTINCT c.nombre_cliente) as total_clientes 
    FROM Clientes c
    WHERE 1=1
    """
    
    # Solo aplicar filtro de ciudad si no es "all"
    if ciudad_seleccionada != 'all':
        query_clientes += f" AND c.ciudad = '{ciudad_seleccionada}'"
    
    df_clientes = pd.read_sql(query_clientes, conn)
    total_clientes = df_clientes['total_clientes'].iloc[0]
    
    # Construir consulta de productos con filtros
    query_productos = """
    SELECT COUNT(DISTINCT p.id_producto) as total_productos 
    FROM Productos p
    JOIN Detalles_Ventas dv ON p.id_producto = dv.id_producto
    JOIN Ventas v ON dv.id_venta = v.id_venta
    JOIN Clientes c ON v.id_cliente = c.id_cliente
    WHERE 1=1
    """
    
    # Aplicar filtros si no son "all"
    if ciudad_seleccionada != 'all':
        query_productos += f" AND c.ciudad = '{ciudad_seleccionada}'"
    
    if categoria_seleccionada != 'all':
        query_productos += f" AND p.categoria = '{categoria_seleccionada}'"
    
    df_productos = pd.read_sql(query_productos, conn)
    total_productos = df_productos['total_productos'].iloc[0]
    
    # Obtener el total del catálogo (100) - ANTES de cerrar la conexión
    query_catalogo = "SELECT COUNT(*) as total_catalogo FROM Productos"
    df_catalogo = pd.read_sql(query_catalogo, conn)
    total_catalogo = df_catalogo['total_catalogo'].iloc[0]
    
    conn.close()  # Cerrar conexión DESPUÉS de todas las consultas
    
    ticket_promedio = df_filtrado.groupby('id_venta')['importe'].sum().mean()
    
    # Formatear los valores
    ingresos_formateado = "${:,.0f}".format(ingresos_totales) if ingresos_totales > 0 else "$0"
    ticket_formateado = "${:,.0f}".format(ticket_promedio) if pd.notna(ticket_promedio) and ticket_promedio > 0 else "$0"
    
    return (
        ingresos_formateado,
        str(total_ventas),
        str(total_clientes),
        f"{total_productos}/{total_catalogo}",  # ← FORMATO 95/100
        ticket_formateado
    )


# Callbacks para la geoanalítica
@app.callback(
    [Output('mapa-geografico', 'figure'),
     Output('metricas-ciudades', 'figure'),
     Output('distribucion-regional', 'figure'),
     Output('crecimiento-ciudades', 'figure')],
    [Input('metrica-geo', 'value'),
     Input('size-slider', 'value')]
)
def update_geoanalytics(metrica_seleccionada, tamaño_burbuja):
    # Preparar datos para el mapa
    datos_ciudades = []
    
    for ciudad in df['ciudad'].unique():
        df_ciudad = df[df['ciudad'] == ciudad]
        
        if metrica_seleccionada == 'ingresos':
            valor = df_ciudad['importe'].sum()
        elif metrica_seleccionada == 'ventas':
            valor = df_ciudad['id_venta'].nunique()
        elif metrica_seleccionada == 'ticket':
            valor = df_ciudad.groupby('id_venta')['importe'].sum().mean()
        else:  # clientes
            valor = df_ciudad['id_cliente'].nunique()
        
        datos_ciudades.append({
            'ciudad': ciudad,
            'valor': valor,
            'lat': COORDENADAS_CIUDADES[ciudad]['lat'],
            'lon': COORDENADAS_CIUDADES[ciudad]['lon'],
            'ventas': df_ciudad['id_venta'].nunique(),
            'clientes': df_ciudad['id_cliente'].nunique(),
            'ingresos': df_ciudad['importe'].sum()
        })
    
    df_mapa = pd.DataFrame(datos_ciudades)
    
    # 1. Mapa Geográfico
    fig_mapa = px.scatter_mapbox(
        df_mapa,
        lat="lat",
        lon="lon",
        size="valor",
        color="valor",
        hover_name="ciudad",
        hover_data={
            'ventas': True,
            'clientes': True,
            'ingresos': ':.2f',
            'lat': False,
            'lon': False
        },
        size_max=tamaño_burbuja,
        color_continuous_scale=COLOR_PALETTE,
        zoom=7,
        height=600
    )
    
    fig_mapa.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR)
    )
    
    # 2. Métricas por Ciudad (Gráfico de barras)
    fig_metricas = px.bar(
        df_mapa,
        x='ciudad',
        y='valor',
        title=f'{metrica_seleccionada.title()} por Ciudad',
        color='valor',
        color_continuous_scale=COLOR_PALETTE
    )
    
    fig_metricas.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR),
        showlegend=False,
        height=400
    )
    
    # 3. Distribución Regional (Pie chart)
    fig_distribucion = px.pie(
        df_mapa,
        values='valor',
        names='ciudad',
        title=f'Distribución Regional - {metrica_seleccionada.title()}',
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig_distribucion.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR)
    )
    
    # 4. Crecimiento por Ciudad (Simulado - en un caso real usarías datos temporales)
    # Para este ejemplo, simulo un crecimiento basado en los ingresos
    df_mapa['crecimiento'] = df_mapa['valor'] / df_mapa['valor'].sum() * 100
    
    fig_crecimiento = px.bar(
        df_mapa,
        x='ciudad',
        y='crecimiento',
        title='Participación por Ciudad (%)',
        color='crecimiento',
        color_continuous_scale=COLOR_PALETTE
    )
    
    fig_crecimiento.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=TEXT_COLOR),
        showlegend=False,
        height=400
    )
    
    return fig_mapa, fig_metricas, fig_distribucion, fig_crecimiento


# Ejecutar la aplicación
if __name__ == '__main__':

    try:
        app.run(debug=True, port=8050)
    except OSError:
        print("🔄 Puerto 8050 ocupado, usando puerto 8051...")
        app.run(debug=True, port=8051)