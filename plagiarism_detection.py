import re
import string
import heapq
import sys

# Utility Class for Text Processing and Distance Calculation
class TextUtils:
    @staticmethod
    def preprocess_text(text):
        """
        Preprocesses text by converting to lowercase, removing punctuation, and tokenizing into sentences.
        """
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]

    @staticmethod
    def levenshtein_distance(s1, s2):
        """
        Computes the Levenshtein distance between two strings.
        """
        if len(s1) < len(s2):
            return TextUtils.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        # Initialize distance matrix
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

# Heuristic Function Class
class Heuristic:
    @staticmethod
    def estimate_remaining_cost(remaining1, remaining2):
        """
        Estimates the heuristic cost based on the number of remaining sentences.
        """
        return min(len(remaining1), len(remaining2))

# A* Search Class for Sentence Alignment
class SentenceAligner:
    def __init__(self, sentences1, sentences2):
        self.sentences1 = sentences1
        self.sentences2 = sentences2
        self.visited = set()

    def a_star_search(self):
        """
        Uses A* search to find the optimal alignment cost between two sets of sentences.
        """
        pq = []
        initial_state = (0, 0, 0)  # (index in doc1, index in doc2, cost)
        heapq.heappush(pq, (0, initial_state))

        while pq:
            _, (i, j, cost) = heapq.heappop(pq)

            if i == len(self.sentences1) and j == len(self.sentences2):
                return cost

            if (i, j) in self.visited:
                continue
            self.visited.add((i, j))

            # Align current sentences
            if i < len(self.sentences1) and j < len(self.sentences2):
                align_cost = cost + TextUtils.levenshtein_distance(self.sentences1[i], self.sentences2[j])
                heapq.heappush(pq, (align_cost + Heuristic.estimate_remaining_cost(self.sentences1[i+1:], self.sentences2[j+1:]), (i+1, j+1, align_cost)))

            # Skip sentence in doc1
            if i < len(self.sentences1):
                skip_cost = cost + 1  # Penalty for skipping
                heapq.heappush(pq, (skip_cost + Heuristic.estimate_remaining_cost(self.sentences1[i+1:], self.sentences2[j:]), (i+1, j, skip_cost)))

            # Skip sentence in doc2
            if j < len(self.sentences2):
                skip_cost = cost + 1  # Penalty for skipping
                heapq.heappush(pq, (skip_cost + Heuristic.estimate_remaining_cost(self.sentences1[i:], self.sentences2[j+1:]), (i, j+1, skip_cost)))

        return float('inf')

# Plagiarism Detector Class
class PlagiarismDetector:
    def __init__(self, doc1, doc2, threshold=200):
        self.doc1 = doc1
        self.doc2 = doc2
        self.threshold = threshold
        self.sentences1 = TextUtils.preprocess_text(doc1)
        self.sentences2 = TextUtils.preprocess_text(doc2)

    def detect_plagiarism(self):
        """
        Detects plagiarism based on a given Levenshtein distance threshold.
        """
        potential_plagiarism = []
        for i, sentence1 in enumerate(self.sentences1):
            for j, sentence2 in enumerate(self.sentences2):
                dist = TextUtils.levenshtein_distance(sentence1, sentence2)
                print(f"Distance between sentence {i+1} in Document 1 and sentence {j+1} in Document 2: {dist}")
                if dist <= self.threshold:
                    potential_plagiarism.append((i, j, dist))  # (Index in doc1, Index in doc2, Distance)
        return potential_plagiarism

    def run_detection(self):
        """
        Executes the A* search for alignment cost and detects plagiarism.
        """
        aligner = SentenceAligner(self.sentences1, self.sentences2)
        alignment_cost = aligner.a_star_search()
        plagiarized_sentences = self.detect_plagiarism()
        return alignment_cost, plagiarized_sentences

# Main function for execution
def main():
    print("Enter the first document (multi-line, end with Ctrl+D):")
    doc1 = sys.stdin.read().strip()

    print("\nEnter the second document (multi-line, end with Ctrl+D):")
    doc2 = sys.stdin.read().strip()

    # Create a PlagiarismDetector instance and run detection
    detector = PlagiarismDetector(doc1, doc2)
    alignment_cost, plagiarized_sentences = detector.run_detection()

    # Output the results
    print("\nAlignment Cost:", alignment_cost)
    print("\nPlagiarized Sentence Pairs (Doc1 Index, Doc2 Index, Distance):")
    for i, j, dist in plagiarized_sentences:
        print(f"Sentence {i+1} in Document 1 and Sentence {j+1} in Document 2 with a distance of {dist}")

# Calling the main function
if __name__ == "__main__":
    main()
