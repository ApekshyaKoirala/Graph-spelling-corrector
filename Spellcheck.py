from collections import defaultdict, deque

class GraphNode:
    def __init__(self,char):
        self.char=char
        self.neighbours=set()
        self.is_end_of_word=False

class GraphSpellChecker:
    def __init__(self):
        self.root=GraphNode(' ')

    def insert(self,word):
        node=self.root
        for char in word:
            found=False
            for neighbour in node.neighbours:
                if neighbour.char==char:
                    node=neighbour
                    found=True
                    break
            if not found:
                new_node=GraphNode(char)
                node.neighbours.add(new_node)
                node=new_node
        node.is_end_of_word=True

    def search(self,word):
        node=self.root
        for char in word:
            found=False
            for neighbour in node.neighbours:
               if neighbour.char==char:
                   node=neighbour
                   found=True
                   break
            if not found:
                return False
        return node.is_end_of_word
    
    def get_suggestions(self,prefix):
        node=self.root
        for char in prefix:
            found=False
            for neighbour in node.neighbours:
                if neighbour.char==char:
                    node=neighbour
                    found=True
                    break
            if not found:
                return []
            
        suggestions=[]
        queue=deque()
        queue.append((node,prefix))
        while queue:
            current_node, current_word=queue.popleft()
            if current_node.is_end_of_word:
                suggestions.append(current_word)
            for neighbour in current_node.neighbours:
                queue.append((neighbour,current_word+neighbour.char))
        return suggestions
    
def load_dictionary(graph, file_path):
        with open(file_path, 'r') as file:
            for word in file:
                graph.insert(word.strip())

def spell_check(graph,word):
        if graph.search(word):
            print(f"{word} is spelled correctly.")
        else:
            print(f"'{word}' is misspelled.")
            suggestions=graph.get_suggestions(word[:3])
            if suggestions:
                print("Did you mean:")
                for suggestion in suggestions[:5]:
                    print(f"-{suggestion}")
            else:
                print('NO suggestion found.')



if __name__ == "__main__":
    graph = GraphSpellChecker()
    load_dictionary(graph, "words.txt")  # Load the dictionary

    while True:
        word = input("Enter a word to check (or 'exit' to quit): ").strip().lower()
        if word == "exit":
            break
        spell_check(graph, word)
