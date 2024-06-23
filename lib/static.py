
email_document = """

<!doctype html>
<html lang="en">

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>MorningNooz</title>
    <style media="all" type="text/css">
        @media all {
            .btn-primary table td:hover {
                background-color: #b96eff !important;
            }

            .btn-primary a:hover {
                background-color: #b96eff !important;
                border-color: #b96eff !important;
            }
        }

        @media only screen and (max-width: 640px) {

            .main p,
            .main td,
            .main span {
                font-size: 16px !important;
            }

            .wrapper {
                padding: 8px !important;
                padding-left: 12px !important;
                padding-right: 12px !important;
            }

            .content {
                padding: 0 !important;
            }

            .container {
                padding: 0 !important;
                padding-top: 8px !important;
                width: 100% !important;
            }

            .main {
                border-left-width: 0 !important;
                border-radius: 4px !important;
                border-right-width: 0 !important;

            }
            h2 {
                margin-top: 8px;
            }

            .btn table {
                max-width: 100% !important;
                width: 100% !important;
            }

            .btn a {
                font-size: 16px !important;
                max-width: 100% !important;
                width: 100% !important;
            }
        }

        @media all {
            .ExternalClass {
                width: 100%;
            }

            a {
                color: #5a189a;
            }

            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {
                line-height: 100%;
            }

            .apple-link a {
                color: inherit !important;
                font-family: inherit !important;
                font-size: inherit !important;
                font-weight: inherit !important;
                line-height: inherit !important;
                text-decoration: none !important;
            }

            #MessageViewBody a {
                color: inherit;
                text-decoration: none;
                font-size: inherit;
                font-family: inherit;
                font-weight: inherit;
                line-height: inherit;
            }
        }
    </style>
</head>

<body
    style="font-family: Helvetica, sans-serif; -webkit-font-smoothing: antialiased; font-size: 16px; line-height: 1.3; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background-color: #f4f4f486; margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body"
        style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; /*background-color: #E1D7FF; */ width: 100%;"
        width="100%"
        >
        <tr>
            <td>

            </td>
        </tr>
        <tr>
            <td style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top;" valign="top">&nbsp;
            </td>
            <td class="container"
                style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top; max-width: 600px; padding: 0; padding-top: 24px; width: 600px; margin: 0 auto; "
                
                width="600" valign="top">
                <h1 style="text-align: center; font-size: 40px;">MorningNooz</h1>
                <div class="content"
                    style="box-sizing: border-box; display: block; margin: 0 auto; max-width: 600px; padding: 0;">

                    <!-- START CENTERED WHITE CONTAINER -->
                    <span class="preheader"
                        style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">
                        Your personal news digest!</span>
                    
                    <!-- TOPIC ENTRY TABLES -->
                    
                    $entries

                    <!-- START FOOTER -->
                    <div class="footer" style="clear: both; padding-top: 24px; text-align: center; width: 100%;">
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;"
                            width="100%">
                            <tr>
                                <!-- <td class="content-block"
                                    style="font-family: Helvetica, sans-serif; vertical-align: top; color: #9a9ea6; font-size: 16px; text-align: center;"
                                    valign="top" align="center">
                                    <br> Don't like these emails? <a href="http://htmlemail.io/blog"
                                        style="text-decoration: underline; color: #9a9ea6; font-size: 16px; text-align: center;">Unsubscribe</a>.
                                </td> -->
                            </tr>
                            <tr>
                                <td class="content-block powered-by"
                                    style="font-family: Helvetica, sans-serif; vertical-align: top; color: #9a9ea6; font-size: 16px; text-align: center;"
                                    valign="top" align="center">
                                    Change your preferences at <a href="https://morningnooz.com"
                                        style="color: #9a9ea6; font-size: 16px; text-align: center; text-decoration: none;">MorningNooz.com</a>
                                </td>
                            </tr>
                        </table>
                    </div>

                    <!-- END FOOTER -->

                    <!-- END CENTERED WHITE CONTAINER -->
                </div>
            </td>
            <td style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top;" valign="top">&nbsp;
            </td>
        </tr>
        <br/><br/>
    </table>
</body>

</html>


"""


single_topic_entry = """
<table role="presentation" border="0" cellpadding="0" cellspacing="0" class="main"
    style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background: #ffffff; border: 1px solid #eaebed; border-radius: 16px; width: 100%; margin-bottom: 24px;"
    width="100%">

    <!-- START MAIN CONTENT AREA -->
    <tr>
        <td class="wrapper"
            style="font-family:Arial, Helvetica, sans-serif, sans-serif; font-size: 16px; vertical-align: top; box-sizing: border-box; padding: 24px; padding-top:24px"
            valign="top">
            <h2 style="text-align: start; letter-spacing: 0.5px; margin-bottom: 12px;  border-bottom: #5a189a; border-width: 0px 0px 4px 0px; border-style:solid;">
              $topic
            </h2>
            $chunks
        </td>
    </tr>

</table>

"""

summary_chunk = """
<h3 style="font-family: Helvetica, sans-serif; margin: 0; margin-bottom: 8px; font-weight: 600;">
    $title
</h3>
<p style="font-family: Helvetica, sans-serif; font-size: 16px; font-weight: normal; margin: 0; margin-bottom: 16px;">
    $summary
</p>

"""


# archive ---

topic_summary_template_flex = """
<div style="display: flex; flex-direction: column; background: linear-gradient(300deg, #977FDD, #BAA5F3); border-radius: 20px; padding:24px; width: fit-content; color:white">
    <h3 style="margin-left: 16px">$topic</h3>
    <br>
    <div style="display: flex; flex-direction: row; flex-wrap: wrap;">
        $entries
    </div>
</div>
"""

topic_summary_template_table = """
<div style="width: 100%;" align="center">
    <table align="center" style="background-color: #977fdd;border-radius:8px;padding:8px;width:fit-content;color:#000000;">
    <tr class="gmail-blend-difference">
        <td>&nbsp;</td>
        <td class="gmail-blend-difference" style="vertical-align: top;">
                <h1>$topic</h1>
        </td>
    </tr>
    <tr>
            <td>&nbsp;</td>
            <td>
                <table>
                    $entries
                </table>
            </td>
            <td>&nbsp;</td>
    </tr>
    </table>
</div>
"""

topic_entry_template = """
<tr>
    <td class="gmail-blend-difference" style="color: #000000; max-width:456px; margin: 16px; border-radius: 12px; background-color: #6848C1;overflow: hidden; padding: 1rem; position: relative; ">
        <div class="gmail-blend-difference"  style="background-color: #FFFFFF; background-size: cover; border-radius: 8px; padding:20px; mix-blend-mode: normal;">
            
                    <h3>$title</h3>
                    <p>$summary</p>
               
        </div>
    </td>
</tr>
<tr>&nbsp;</tr>
"""

closing_message = """
<hr>
<p>
    <em>
        Thanks so much for trying out the beta of MorningNooz! Learn more and change your topics at <a href="https://morningnooz.com">morningnooz.com</>
    </em>
</p>
"""

style_sheet = """
<style type="text/css">
    u + .body .gmail-blend-difference { background:#FFF; mix-blend-mode:difference; }
</style>
"""

error_template = """
{
      "summaries": []
}
"""
