with open('tshet.dict.yaml') as f1, \
        open('tshet.words.dict.yaml') as f2, \
        open('tshet_unspaced.dict.yaml', 'w') as g:
    # Header f1
    for line in f1:
        if line == '...\n':
            g.write(line)
            break
        else:
            # Override several configurations
            if line == '# encoding: utf-8\n':
                g.write(line)
                g.write('#\n# NOTICE: This file is auto-generated for reverse lookup.\n')
                g.write('# Do not edit this file directly!\n')
                g.write('# You should edit tshet.dict.yaml and tshet.words.dict.yaml.\n')
            elif line == 'name: tshet\n':
                g.write('name: tshet_unspaced\n')
            elif line in [
                'use_preset_vocabulary: true\n',
                'import_tables:\n',
            ] or line.startswith('  - '):
                pass
            else:
                g.write(line)

    # Dictionary f1
    for line in f1:
        if line.startswith('#'):
            g.write(line)
        else:
            g.write(line.replace(' ', '='))

    # Header f2
    for line in f2:
        if line == '...\n':
            break

    # Dictionary f2
    for line in f2:
        if line.startswith('#'):
            g.write(line)
        else:
            g.write(line.replace(' ', '='))
