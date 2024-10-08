def export_html_report(comparison_results, file_path):
    html_content = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #4a4a4a;
            }
            .report-container {
                max-width: 900px;
                margin: 0 auto;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
            .result {
                margin-bottom: 40px;
            }
            h2 {
                font-size: 1.2em;
                margin-bottom: 10px;
            }
            p {
                font-size: 1em;
                margin: 5px 0;
            }
            .visual {
                position: relative;
                background-color: #ddd;
                height: 30px;
                border-radius: 5px;
                margin: 15px 0;
                overflow: hidden;
            }
            .encrypted {
                background-color: #ff4d4d;
                height: 100%;
                position: absolute;
            }
            .ranges {
                font-size: 0.9em;
                color: #666;
            }
            ul {
                padding-left: 20px;
                margin-top: 10px;
            }
            li {
                line-height: 1.5;
            }
            footer {
                text-align: center;
                font-size: 0.85em;
                color: #aaa;
                margin-top: 40px;
            }
        </style>
    </head>
    <body>
        <h1>Cryptalyst Report</h1>
        <div class="report-container">
    """

    for result in comparison_results:
        # Convert file size to a human-readable format
        file_size = result['total_size']
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        elif file_size < 1024 * 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{file_size / (1024 * 1024 * 1024):.2f} GB"

        html_content += f"""
        <div class="result">
            <h2>Original: {result['original_file']}</h2>
            <h2>Encrypted: {result['encrypted_file']}</h2>
            <p><strong>File Size:</strong> {size_str}</p>
            <p><strong>Percentage Encrypted:</strong> {result['percentage_encrypted']:.2f}%</p>
            <div class="visual">
        """
        
        total_size = result['total_size']
        for start, end in result['encrypted_ranges']:
            start_percent = (start / total_size) * 100
            end_percent = (end / total_size) * 100
            width_percent = end_percent - start_percent
            html_content += f'<div class="encrypted" style="width: {width_percent}%; left: {start_percent}%;"></div>'
        
        html_content += """
            </div>
            <p class="ranges"><strong>Encrypted Ranges:</strong></p>
            <ul>
        """
        for start, end in result['encrypted_ranges']:
            html_content += f"<li>Decimal: [{start}, {end}] | Hex: [0x{start:X}, 0x{end:X}]</li>"

        html_content += """
            </ul>
        </div>
        """

    html_content += """
        </div>
        <footer>
            Report generated by Cryptalyst
        </footer>
    </body>
    </html>
    """

    with open(file_path, 'w') as f:
        f.write(html_content)