with open('generate_final_report_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove Figure 1.2 from Chapter 4
old_fig12_ch4 = '# 2. Figure 1.2 Clean Area\nadd_clean_figure_space("Figure 1.2", "Overall System Workflow", empty_lines=14)'
if old_fig12_ch4 in text:
    text = text.replace(old_fig12_ch4, '')
    print('Removed Fig 1.2 from Ch 4')

# 2. Add Figure 1.2 after 1.3.3
marker = 'add_subsec_heading("1.3.3", "State-Wide Inter-Collegiate SaaS Scope")'
idx = text.find(marker)
if idx != -1:
    end_para = text.find(')', idx + 50) + 1
    text = text[:end_para] + '\n\n# 2. Figure 1.2 Clean Area\nadd_clean_figure_space("Figure 1.2", "Overall System Workflow", empty_lines=14)' + text[end_para:]
    print('Added Fig 1.2 after 1.3.3')

with open('generate_final_report_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
