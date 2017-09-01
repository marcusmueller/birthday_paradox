#include <iostream>
#include <string>
#include <fstream>
#include <vector>
/*
 * By fortune of hash_string being from GNU Radio, this file's GPL'ed. 
 */

static unsigned int
hash_string(const std::string &s)
{
  unsigned int h = 0;
  unsigned int g = 0;

  for (std::string::const_iterator p = s.begin(); p != s.end(); ++p){
    h = (h << 4) + (*p & 0xff);
    g = h & 0xf0000000;
    if (g){
      h = h ^ (g >> 24);
      h = h ^ g;
    }
  }
  return h;
}

int main() {
  std::ifstream wordlist ("words.txt");
  if (!wordlist.is_open()) {
    std::string info("Download https://raw.githubusercontent.com/dwyl/english-words/master/words.txt as data basis.\n");
    std::cerr << info;
    return -1;
  }

  std::vector<unsigned> histogram(701);
  std::string line;
  while ( std::getline (wordlist,line) ) {
    unsigned int val = hash_string(line) % 701;
    // std::cout << line << ": " << val << "\n";
    histogram[val]++;
  }
  wordlist.close();
  for(unsigned i = 0; i < 701; i++)
    std::cout << histogram[i] << "\n";
  return 0;
}

