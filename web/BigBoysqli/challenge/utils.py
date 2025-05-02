import random
import string
import hashlib

def generate(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    
    random_string = ''.join(random.choices(characters, k=length))
    
    return random_string

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

banned_list = ["sleep", "delay", "waitfor", "benchmark", "pg_sleep", "randomblob", "delete", "zeroblob", 
                   'abort', 'action', 'add', 'after', 'all', 'alter', 'always', 'analyze', 'and', 'asc', 
                   'attach', 'autoincrement', 'before', 'begin', 'between', 'by', 'cascade', 'case', 'cast', 
                   'check', 'collate', 'column', 'commit', 'conflict', 'constraint', 'create', 'cross', 'current', 
                   'current_date', 'current_time', 'current_timestamp', 'database', 'default', 'deferrable', 'deferred', 
                   'delete', 'desc', 'detach', 'distinct', 'do', 'drop', 'each', 'else', 'end', 'escape', 'except', 'exclude', 
                   'exclusive', 'exists', 'explain', 'fail', 'filter', 'first', 'following', 'for', 'foreign', 'full', 
                   'generated', 'glob', 'group', 'groups', 'having', 'if', 'ignore', 'immediate', 'index', 'indexed', 'initially', 
                   'inner', 'insert', 'instead', 'intersect', 'into', 'is', 'isnull', 'join', 'key', 'last', 'left', 'limit', 'match', 
                   'materialized', 'natural', 'no', 'not', 'nothing', 'notnull', 'null', 'nulls', 'of', 'offset', 'on', 'order', 'others', 
                   'outer', 'over', 'partition', 'plan', 'pragma', 'preceding', 'primary', 'query', 'raise', 'range', 'recursive', 'references', 
                   'regexp', 'reindex', 'release', 'rename', 'replace', 'restrict', 'returning', 'right', 'rollback', 'row', 'rows', 'savepoint', 
                   'table', 'temp', 'temporary', 'then', 'ties', 'to', 'transaction', 'trigger', 'unbounded', 'union', 'unique', 
                   'using', 'vacuum', 'values', 'view', 'virtual', 'when', 'window', 'with', 'without',]