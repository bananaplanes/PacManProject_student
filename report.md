PART 1:

Each group member updated their feature branch. Maya did feature/Pacman, Dillon did feature/item, Lucas did feature/ghost, Burke did feature/game_board. Everyone added tests to test_Pacman.py. Burke added the issue to GitHub in the base repo and test case to show where the code failed for the ghost spawning in the walls. Dillon and Maya reviewed and merged each other's pull requests, Lucas and Burke reviewed and merged each other's pull requests.

PART 2: 

Lucas did PR reviews and merges, writing this report, and helped with renaming player to pacman. Maya did the renaming to pacman (commands shown below). Burke did the "Secure Sensitive Information" section. Dillon did the "Implement a GitHub Actions CI/CD Pipeline" section. 

commands used for renaming player to pacman:
{

    git checkout -b rename-to-pacman

    git ls-files | grep -i player

    for f in $(git grep -l -I player); do
    git mv "$f" "$(echo "$f" | sed 's/[Pp]layer/Pacman/g')";

    grep -RIn "player" .

    sed -I 's/player/Pacman/g; s/Player/Pacman/g' $(git grep -l -I
    player)

    git branch --list "*player*"

    git branch -m feature/player feature/pacman

}