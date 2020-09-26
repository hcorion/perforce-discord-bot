# Perforce Discord bot

This is a discord bot for my personal Perforce server.

Right now it only supports fancy highlighting of [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) via the "commit message with scope" format. Maybe at some point I'll extend it to support some of the more generic conventional commit formats, but this works for now.

This will probably get extended to more Unreal Engine-specific use cases in the future.

## Potentional Future Features

- Add command to queue all the files in a changelist
- Add command to get latest changelist from user
- Add association of Perforce username with Discord username
- Support more of the different conventional commit formats ("fix: body"). Maybe breaking change, but not really relevant to me.
- Add detection of C++ changes in a changelist and send message telling people to recompile on the next pull.

### Stretch Goals:
- Trigger an auto format C++ via clang-format after a changelist (there might be a way to do this within perforce itself)
