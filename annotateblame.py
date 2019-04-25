import os
import subprocess


def write_blame_file(filepath):
    res = subprocess.call('git blame {0}.py > {0}.txt'.format(filepath), shell=True)
    if res != 0:
        raise SystemError('Subprocess failed for {}'.format(filepath))


def get_name(line):
    start_of_name_idx = line.find('(') + 1
    end_of_name_idx = line[start_of_name_idx:].find('20') + start_of_name_idx
    return line[start_of_name_idx:end_of_name_idx].strip()


def process_line(line):
    start_of_code_idx = line.find(')') + 2
    new_line = line[start_of_code_idx:-1] + '  # by ' + get_name(line) + '\n'
    return new_line


if __name__ == '__main__':

    # Add path to file here
    path = 'path/to/file'

    files = [x for x in os.listdir(path) if x.endswith('.py')]
    names = set()

    for m in files:
        filepath = path + '/' + m
        if filepath.endswith('.py'):
            filepath = filepath[:-3]

        write_blame_file(filepath)

        with open(filepath + '.txt', 'r') as blame_file:
            with open(filepath + '.py', 'w') as output:
                for line in blame_file:
                    names.add(get_name(line))
                    output.write(process_line(line))
    print('Names:')
    for name in names:
        print(name)

    for f in files:
        os.remove(path + '/' + f[:-3] + '.txt')
