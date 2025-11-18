# Dity Commands Reference

This document provides a comprehensive reference for all available Dity CLI commands.

## Available Commands

### `drive`

#### `drive scan`

---

The `scan` command looks for newly connected external drives and adds them to the list of known drives, which can be read using `dity drive list`. It finds the drives and scand the folder structure to determine if it fits any of the given drive formats provided in `~/.dity/drive-types`.

When a new drive is found, the user is provided the option to add it as a source drive or destination drive. This can later be changed by using `drive edit` if desired.

#### `drive list`

The `drive list` command allows you to see the current set of drives recognized by dity. To update the list, you may need to run `drive scan` to find new drives.

When you run `drive list` it will return a table of drives with their type and status. For example:

```console
| Drive   | Type     | Status     |
|---------|----------|------------|
| card1   | RED      | Offloaded  |
| card2   | MixPre   | Ready      |
| backup1 | Offload  | Connected  |
```

**Drive** is the name of the actual drive.

**Type** is the format the drive adheres to based on the list of possible drive formats provided in `~/.dity/drive-types`. For example, if the drive has the file structure of a RED camera card, it's listed as RED.

**Status** refers to the status of the drive, which can be `["Ready", "Offloading", "Paused", "Offloaded", "Error"]` for source drives, and `["Connected", "Writing", "Error"]` for destination drives.

#### `drive edit`

---

Edit the information for a given drive. If no name is provided, the user is prompted to select a drive from a list. Once the drive has been specified, the user can modify the drive info, including Name, Format (i.e. type of drive), and if the drive is a source drive or destination drive. The user can specify these with the flags `n` (name), `f` (format), and `t` (type). If no flags are provided, the user is prompted to edit or confirm all three fields.

**Example Usage:**

With name

```bash
dity drive edit card1 # name of card here
```

Without name

```bash
dity drive edit # no name provided
```

```console
Please select the drive you would like to edit:
[1] card1
[2] card2
[3] backup1
[4] backup2
```

Editing the name

```bash
dity drive edit card1 -n # add n flag
```

Editing name and format

```bash
dity drive edit card1 -nf
```

#### `drive eject`

---

Eject a given drive. You can provide the drive to eject or, if no drive is provided, you will be prompted to select which drive to eject. If the drive has not been marked as offloaded, you will need to use the `--force` flag to eject it.

**Example Usage:**

With name

```bash
dity drive eject card1 # name of card here
```

Without name

```bash
dity drive eject # no name provided
```

```console
Please select the drive you would like to eject:
[1] card1
[2] card2
[3] backup1
[4] backup2
```

Force eject

```bash
dity drive eject card1 --force
```

### `offload`

### `proj`
