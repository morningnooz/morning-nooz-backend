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
    <table align="center" style="background-color: #977fdd;border-radius:20px;padding:24px;width:fit-content;color:#000000;">
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
    </tr>
    </table>
</div>
"""

topic_entry_template = """
<tr>
    <td class="gmail-blend-difference" style="color: #000000; width: 256px; margin: 16px; border-radius: 32px; background-color: #6848C1;overflow: hidden; padding: 1rem; position: relative; ">
        <div class="gmail-blend-difference"  style="background-color: #FFFFFF; background-size: cover; border-radius: 20px; padding:20px; mix-blend-mode: normal;">
            
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
