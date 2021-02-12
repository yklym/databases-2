<?xml version = "1.0" encoding = "UTF-8"?>
<!-- xsl stylesheet declaration with xsl namespace: -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="//data">
        <html>
            <head>
                <title>Task 4</title>
                <style type="text/css">
                    .flex-wrapper {
                        display: flex;
                        flex-direction:column;
                        align-items: center;
                    }

                    .item {
                        display: flex;
                        align-items: center;
                        margin: 20px 5px;
                        border: 1px solid black;
                        padding: 5px;
                        width: 90%;
                        justify-content: space-around;
                    }

                    .price {
                        width: 200px;
                    font-size: 2em;
                        font-weight: bolder;
                        text-align: center;
                    }

                    img {
                        width: 400px;
                        height: 400px;
                    }

                    .item-text {
                        width: 500px;
                    }
                </style>
            </head>
            <body>
                <div class="flex-wrapper">

                    <xsl:for-each select="//item">
                        <div class="item">
                            <img>
                                <xsl:attribute name="src">
                                    <xsl:value-of select="./img"/>
                                </xsl:attribute>
                            </img>
                            <div class="item-text">
                                <h2>
                                    <xsl:value-of select="./name"/>
                                </h2>
                                <p>
                                    <xsl:value-of select="./description"/>
                                </p>
                            </div>

                            <p class="price">
                                <xsl:value-of select="./price"/>
                            </p>
                        </div>
                    </xsl:for-each>

                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>