<?php
class Functions
{
    public static function render_template($template, $variables = [])
    {
        $blacklist = [
            'system',
            'exec',
            'shell_exec',
            'passthru',
            'eval',
            'phpinfo',
            'assert',
            'create_function',
            'include',
            'require',
            'fopen',
            'fwrite',
            'file_put_contents',
            'file_get_contents',
        ];
        foreach ($blacklist as $badword) {
            if (stripos($template, $badword) !== false) {
                return "Error: Invalid input detected.";
            }
        }
        extract($variables);
        try {
            eval ("\$output = \"$template\";");
            return $output;
        } catch (ParseError $e) {
            return "Syntax Error: " . $e->getMessage();
        }
    }
}