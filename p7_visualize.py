import json
import sys
import collections

def parse_json_result(out):
    """Parse the provided JSON text and extract a dict
    representing the predicates described in the first solver result."""

    result = out
    
    assert len(result['Call']) > 0
    assert len(result['Call'][0]['Witnesses']) > 0
    
    witness = result['Call'][0]['Witnesses'][0]['Value']
    
    class identitydefaultdict(collections.defaultdict):
        def __missing__(self, key):
            return key
    
    preds = collections.defaultdict(set)
    env = identitydefaultdict()
    
    for atom in witness:
        if '(' in atom:
            left = atom.index('(')
            functor = atom[:left]
            arg_string = atom[left:]
            try:
                preds[functor].add( eval(arg_string, env) )
            except TypeError:
                pass # at least we tried...
            
        else:
            preds[atom] = True
    
    return dict(preds)

def render_ascii_dungeon(design):
    """Given a dict of predicates, return an ASCII-art depiction of the a dungeon."""
    
    sprite = dict(design['sprite'])
    param = dict(design['param'])
    width = param['width']
    glyph = dict(space='.', wall='W', altar='a', gem='g', trap='_')
    block = ''.join([''.join([glyph[sprite.get((r,c),'space')]+' ' for c in range(width)])+'\n' for r in range(width)])
    return block

def main(args):
	try:
		file = open(args[1])
		json_file = json.load(file)
		file.close()
		
		map = parse_json_result(json_file)
		print render_ascii_dungeon(map)
	except IndexError:
		return False
	 
if __name__ == "__main__":
	sys.exit(not main(sys.argv))