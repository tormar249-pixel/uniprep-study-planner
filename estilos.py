
import streamlit as st


def aplicar_estilos():

    st.markdown(
        """
        <style>

        /* CONTENEDOR PRINCIPAL */

        .block-container {
            max-width: 1150px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: #173A77;
        }

        /* ENCABEZADO */

        .uniprep-hero {
            background: linear-gradient(
                120deg,
                #102A56,
                #174A8B,
                #2563EB
            );

            border-radius: 22px;
            padding: 40px;
            margin-bottom: 30px;

            box-shadow:
                0 12px 30px rgba(18, 51, 102, 0.15);
        }

        .uniprep-etiqueta {
            color: #C8DBFF;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
        }

        .uniprep-titulo {
            color: white;
            font-size: 40px;
            font-weight: 800;
            margin-top: 12px;
        }

        .uniprep-descripcion {
            color: #E3ECFF;
            font-size: 16px;
            line-height: 1.7;
            max-width: 700px;
            margin-top: 14px;
            margin-bottom: 0;
        }

        /* FORMULARIO */

        [data-testid="stForm"] {
            background: #FFFFFF;
            border: 1px solid #DFE7F3;
            border-radius: 18px;
            padding: 25px;
            box-shadow:
                0 6px 22px rgba(20, 49, 91, 0.05);
        }

        /* BOTONES */

        div.stFormSubmitButton button {
            background: #2563EB;
            color: white;
            border: none;
            border-radius: 10px;
            min-height: 46px;
            font-weight: 600;
        }

        div.stFormSubmitButton button:hover {
            background: #174AAB;
            color: white;
        }

        div.stDownloadButton button {
            background: #173A77;
            color: white;
            border: none;
            border-radius: 10px;
            min-height: 46px;
            font-weight: 600;
        }

        div.stDownloadButton button:hover {
            background: #2563EB;
            color: white;
        }

        /* TARJETAS DE MÉTRICAS */

        [data-testid="stMetric"] {
            background: white;
            border: 1px solid #DFE7F3;
            border-radius: 15px;
            padding: 18px;
        }

        [data-testid="stMetricValue"] {
            color: #174A8B;
            font-weight: 800;
        }

        /* TARJETAS DEL CALENDARIO */

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px;
        }

        /* TÉCNICAS DESPLEGABLES */

        [data-testid="stExpander"] {
            background: white;
            border: 1px solid #DFE7F3;
            border-radius: 12px;
        }

        /* PIE DE PÁGINA */

        .uniprep-footer {
            margin-top: 50px;
            padding-top: 24px;
            border-top: 1px solid #DFE7F3;
            text-align: center;
            color: #64748B;
            font-size: 13px;
            line-height: 1.8;
        }

        /* DISEÑO PARA CELULARES */

        @media (max-width: 768px) {

            .uniprep-hero {
                padding: 25px;
            }

            .uniprep-titulo {
                font-size: 28px;
            }

            .uniprep-descripcion {
                font-size: 14px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )
