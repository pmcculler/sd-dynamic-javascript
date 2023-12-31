# sd-dynamic-javascript
Automatic1111 extension that allows embedding Javascript into prompts.

## Javascript!

You can write Javascript now to your heart's content! Examples of how this works after a short preamble, or you can scroll straight to them below.

## Motivation

* Currently you can't embed Javascript in your SD prompts, which is just silly.
* That's sufficent, I think. I can't wait to see what amazing things people come up with. Please share them with me, and others, if you pease.
* There are interfaces for programming with python (via --allow-code and the script dropdown) or with lua (via a different extension) but these fine methods allow you to program the *process* of generating images. Literally there's an 'image.process(512, 512, "a dog playing by the seashore")' kind of API. This extension does not give you the power to program the process or Automatic1111 itself; those do. This extension focuses on embedding & executing Javascript directly in prompts. Whether that is more useful is up to you.

## State: Current Problems and TODOs
* None. Unlike everything else in life, this is problem free.
* Except... it might be something of a security issue to run arbitrary Javascript inside your prompt. Just saying. I mean, there's precautions; the extension uses a headless browser, and those are reasonably well sandboxed. Still.
* And you do have to install something on the side, see Requirements just below. Hey, they say nothing free is worthwhile.

## Requirements

This extension uses selenium and requires that you have a browser driver in your path, I recommend <a href="https://chromedriver.chromium.org/downloads">chromedriver</a> (Mac, Linux, Windows all supported; if you're using, like, BeOS - well, let me know.) As far as I know you really need this, and you have to do it separately from just installing the extension. Sorry. If you know a better way to execute Javascript in an embedded context like this, please let me know.
The extension should take care of installing selenium itself, let me know if you encounter a problem with how that works.

## Capabilities

It's Javascript, executes as if in a browser. I don't know how crazy you can get, please let me know!

## Interation with Other Extension such as Dynamic Prompts

#### Dynamic Prompts
* That magnificent extension does its own thing and as far as I can tell there is no adverse interaction between this extension and that one.
* Dynamic Javascript prompts runs before Dynamic Prompts, so you can create dynamic prompt material with Javascript. The opposite is not true, but something I am considering. Let me know if you have a use for also being able to execute dynamic javascript _after_ dynamic prompts.

#### Lua
* This extension currently does not work with the Lua extension, probably because the Lua extension has its own prompt box. If there is demand, I will look into supporting this.

#### Custom Code Python Script "--allow-code" 
* This integration works just fine today.

## Code, Evaluation, and Order of Evaluation

* Dynamic Javascript prompts runs before Dynamic Prompts, so you can create dynamic prompt material with Javascript.
*  * But you can't include Javascript from a file with Dynamic Prompts, for example, because that Javascript won't get evaluated. LMK if you need that though.
* Code blocks are demarcated by '%%' at the beginning and end. - if that doesn't work for you let me know. I can make it configurable.
* *  e.g. %% console.log(hello world); %%
* Whatever your Javascript returns is what the code block is replaced with. If you return nothing, the code is evaluated but only empty space replaces the code block in the prompt. If you're disappointed by this let me know.
* Positive prompts are evaluated first, then negative prompts.
* Evaluation in each prompt is done in one pass from beginning to end.
* Context for variables is shared among embeddings and between positive and negative prompts (though because of order of exaluation, as mentioned above, it's one-way.)
* Context is cleared between generations. If you expected or need something else, let me know.
* Syntax and other errors will be sent to the console and the prompt.
* *  e.g. Message: javascript error: Unexpected identifier 'able' (Session info: headless chrome=114.0.5735.248) 
* * *    Stacktrace: Backtrace: GetHandleVerifier [0x00F5A813+48355] (No symbol)
* * *    ...
* It does cost a bit to run this every time, not too much, and I haven't measured it, data and anecdotes welcomed.

## Settings

There are no settings, but there's an Enable/Disable Dynamic Javascript option in the webui that does exactly what a reasonable person would expect.

![](assets/enable_checkbox.png)

If you disable it, code blocks will appear in your output, and it costs virtually nothing to execute. If you think disabled Javascript code blocks should disappear instead of showing in the output prompt, let me know.

## Examples

Using screenshots is cheap and easy, but not very accessible and may have other problems. If this causes you any kind of difficulty let me know, I will make changes.

### Basics

```javascript
%% {
  return "the code block value in the prompt becomes what's in quotes";
} %%
```

Begets:

```
the code block value in the prompt becomes what's in quotes
```

You don't need to separate this into separate lines and use braces like I did.

```javascript
%% return "the code block value in the prompt becomes what's in quotes"; %%
```

Begets:

```
the code block value in the prompt becomes what's in quotes
```

I just like the braces and such :shrug:

### Javascript Functions

Stuff like Date() and the console are indeed available.

Date

```javascript
%% {
 return Date();
} %%
```

![](assets/example_date/resault.png)

Bit of a tangent: the results you get when you use just a date as the prompt are curious.

Console

![](assets/example_console_log/command.png)

![](assets/example_console_log/result.png)

### Context

Within a particular generation, variables in one code block can be used by subsequent (later) code blocks.

![](assets/example_shared_context_in_prompt/command.png)

![](assets/example_shared_context_in_prompt/result.png)

This works from the positive prompt to the negative too.

![](assets/example_shared_context_across_prompts/command.png)

![](assets/example_shared_context_across_prompts/result.png)

...but only in the positive->negative direction, because that's the order of evaluation. If you need something else, I guess OOE could be a setting? Let me know.


### A little more complicated

```javascript
%%
function randomInt(min, max) { // min inclusive, max exclusive
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
}

function randomWord() {
  randomWord = "";
  length = randomInt(6,11);
  for (i = 0; i < length; i++) {
    char = 'abcdefghijklmnopqrstuvwxyz1234567890'.charAt([randomInt(0,36)])
    randomWord = randomWord.concat(char);
  }
  console.log(randomWord);
  return randomWord;
}

function randomNumber() {
  randomNumber = "";
  length = randomInt(6,11);
  for (i = 0; i < length; i++) {
    char = '1234567890'.charAt([randomInt(0,10)])
    randomNumber = randomNumber.concat(char);
  }
  console.log(randomNumber);
  return randomNumber;
}
return randomWord() + " " + randomNumber();
%%
```

Begets:

```
4c3ahwn 8893525278
```

I just know you were waiting to have random junk thrown into your prompts.

### Dynamic Prompts

Since this extension runs before Dynamic Prompts, any dynamic prompting you create will work as you might hope. If you need it to run *after*... well, leave a note about that and describe your scenario, please.

![](assets/example_interaction_with_dyamic_prompts/command.png)

![](assets/example_interaction_with_dyamic_prompts/result.png)

## Colophon

Made for fun. I hope if brings you great joy, and perfect hair forever. Contact me with questions and comments, but not threats, please. And feel free to contribute! Pull requests and ideas in Discussions or Issues will be taken quite seriously!

A dog playing by the seashore thanks you for your time.

![](assets/dog.png)
